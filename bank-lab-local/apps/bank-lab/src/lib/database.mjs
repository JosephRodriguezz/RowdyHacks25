import pg from 'pg';

const connectionString = process.env.DATABASE_URL;
const pool = new pg.Pool({connectionString, max: 4, connectionTimeoutMillis: 3000,
  idleTimeoutMillis: 10000, statement_timeout: 5000});
// Log only a stable category; database errors can contain credentials and SQL.
pool.on('error', () => console.error('bank.database.unavailable'));

/**
 * @template T
 * @param {(db: {query: (text: string, values?: unknown[]) => Promise<{rows: any[]}>}) => Promise<T>} callback
 * @returns {Promise<T>}
 */
export async function transaction(callback) {
  if (!connectionString) throw new Error('Database not configured');
  const client = await pool.connect();
  try {
    await client.query('BEGIN');
    // The private reset obtains the same lock: requests cannot see partial seeds.
    await client.query('SELECT pg_advisory_xact_lock(260026)');
    const result = await callback(client);
    await client.query('COMMIT');
    return result;
  } catch (error) {
    await client.query('ROLLBACK').catch(() => {});
    throw error;
  } finally { client.release(); }
}
