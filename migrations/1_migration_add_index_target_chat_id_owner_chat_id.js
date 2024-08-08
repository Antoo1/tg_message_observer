db.getSiblingDB(process.env.MONGO_INITDB_DATABASE).auth(
    process.env.MONGO_INITDB_USERNAME,
    process.env.MONGO_INITDB_PASSWORD
);
db.createCollection("rules");
db.rules.createIndex(
    {
        target_chat_id: 1,
        owner_chat_id: 1,
    },
    {
        unique: true,
        name: 'rules_target_chat_id_owner_chat_id'
    }
);
