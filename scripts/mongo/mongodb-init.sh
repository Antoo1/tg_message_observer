#!/bin/bash

MONGO_REPL_HOSTNAME=${MONGO_REPL_HOSTNAME:-localhost}
MONGO_REPL_ID=${MONGO_REPL_ID:-rs0}  # keep in sync with mongo '--replSet' arg

AFTER_INIT_SCRIPT=/tmp/mongo_after_init.sh
WAIT_MONGO_SLEEP_SEC=1
WAIT_MONGO_TRY_COUNT=30


echo "set post-init task to config replica at '$MONGO_REPL_HOSTNAME'..."
cat <<EOFSH >$AFTER_INIT_SCRIPT
#!/bin/bash

wait_mongo() {
  echo "wait until mongo node is started..."
  for _ in \$(seq $WAIT_MONGO_TRY_COUNT); do
    sleep $WAIT_MONGO_SLEEP_SEC
    mongosh "$MONGO_REPL_HOSTNAME" --eval "quit(0)" && return 0
  done
  return 1
}

if ! wait_mongo; then
  echo "init replica fails: cannot connect mongo node after $WAIT_MONGO_TRY_COUNT tries"
  exit 1
fi

echo "init replica '$MONGO_REPL_ID' at '$MONGO_REPL_HOSTNAME'..."
mongosh "$MONGO_REPL_HOSTNAME" <<-EOFJS

  rs.initiate({
    _id: "$MONGO_REPL_ID",
    members: [ { _id: 0, host: "$MONGO_REPL_HOSTNAME" } ]
  })

EOFJS

echo "create test db '$MONGO_INITDB_DATABASE' and user '$MONGO_INITDB_USERNAME'..."
mongosh "$MONGO_REPL_HOSTNAME" <<-EOFJS

db.getSiblingDB("$MONGO_INITDB_DATABASE").runCommand({
  createUser: "$MONGO_INITDB_USERNAME",
  pwd: "$MONGO_INITDB_PASSWORD",
  roles: ["readWrite"]
})

EOFJS

EOFSH

bash -c ". $AFTER_INIT_SCRIPT; rm $AFTER_INIT_SCRIPT" &
