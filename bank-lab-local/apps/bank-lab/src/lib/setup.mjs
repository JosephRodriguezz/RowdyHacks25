export function validateDatabasePasswords(adminUrl, appPassword) {
  const adminPassword = new URL(adminUrl).password;
  if (!/^[a-f0-9]{32,}$/.test(adminPassword) || !/^[a-f0-9]{32,}$/.test(appPassword || '') ||
      adminPassword === appPassword) {
    throw new Error('Use different database passwords with 32+ hexadecimal characters');
  }
}

export async function provisionAppRole(db, password) {
  if (!/^[a-f0-9]{32,}$/.test(password || '')) throw new Error('Application DB password must be 32+ hex characters');
  // Identifier is fixed; password is validated hex before this DDL is composed.
  await db.query(`DO $$ BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'bank_app') THEN
      CREATE ROLE bank_app LOGIN PASSWORD '${password}';
    ELSE ALTER ROLE bank_app PASSWORD '${password}'; END IF;
  END $$;
  REVOKE ALL ON SCHEMA bank FROM PUBLIC;
  GRANT USAGE ON SCHEMA bank TO bank_app;
  GRANT SELECT ON bank.state, bank.users, bank.accounts, bank.vault, bank.sessions TO bank_app;
  GRANT INSERT, DELETE ON bank.sessions TO bank_app;
  GRANT INSERT ON bank.events TO bank_app;
  GRANT USAGE, SELECT ON SEQUENCE bank.events_sequence_seq TO bank_app;`);
}
