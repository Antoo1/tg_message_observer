db.getSiblingDB('admin').auth(
    process.env.MONGO_INITDB_ROOT_USERNAME,
    process.env.MONGO_INITDB_ROOT_PASSWORD
);
db.createUser({
    user: process.env.MONGO_INITDB_USERNAME,
    pwd: process.env.MONGO_INITDB_PASSWORD,
    roles: [{role: "dbOwner", db: process.env.MONGO_INITDB_DATABASE}]
});