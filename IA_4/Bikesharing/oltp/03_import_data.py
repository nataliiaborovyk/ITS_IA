"""
CASE STUDY: Sistema di Bike Sharing Europeo (Dataset Reale)
Parte 1: Import dei Dati CSV nel Database PostgreSQL

Questo script importa i file CSV del dataset reale nel database OLTP.
"""

import random
from pathlib import Path

import pandas as pd
import psycopg2


# =============================================================================
# CONFIG
# =============================================================================

DB_CONFIG = {
    "dbname": "bikesharing_oltp",
    "user": "postgres",
    "password": "postgres",
    "host": "its_postgresql",
    "port": 5432,
}

# DATA_DIR = Path("/home/python.1/case_study_bikesharing/case_study_bikesharing_real/data")
DATA_DIR = Path("/home/ITS_IA/IA_4/Bikesharing/data")


# =============================================================================
# HELPERS
# =============================================================================

def py_value(x):
    """NaN/NaT -> None, numpy scalar -> Python native via .item()."""
    if pd.isna(x):
        return None
    if hasattr(x, "item"):
        try:
            return x.item()
        except Exception:
            pass
    return x


def assert_csv_exists(filename: str) -> Path:
    p = DATA_DIR / filename
    if not p.exists():
        raise FileNotFoundError(f"File CSV non trovato: {p}")
    return p


def connect_db():
    return psycopg2.connect(**DB_CONFIG)


def make_heavy_user_sampler(user_ids, alpha=1.2):
    """
    Ritorna una funzione che estrae user_id con distribuzione "heavy tail":
    pochi utenti fanno tanti viaggi, tanti utenti ne fanno pochi.
    alpha più alto => più concentrazione su pochi utenti.
    """
    # ordina per avere ranking stabile
    ids = list(user_ids)
    # pesi ~ 1 / rank^alpha
    weights = [1.0 / ((i + 1) ** alpha) for i in range(len(ids))]
    def sample_one():
        return random.choices(ids, weights=weights, k=1)[0]
    return sample_one


# =============================================================================
# IMPORT DIMENSIONS
# =============================================================================

def import_cities(conn):
    print("Importazione cities...")
    df = pd.read_csv(assert_csv_exists("cities.csv"))

    cur = conn.cursor()
    try:
        for _, row in df.iterrows():
            cur.execute(
                """
                INSERT INTO cities (id, name, lat, lon, timezone, country, return_to_official_only)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
                """,
                (
                    py_value(row["id"]),
                    py_value(row["name"]),
                    py_value(row["lat"]),
                    py_value(row["lon"]),
                    py_value(row["timezone"]),
                    py_value(row["country"]),
                    py_value(row.get("return_to_official_only")),
                ),
            )
        conn.commit()
        print(f"✓ {len(df)} città importate")
    finally:
        cur.close()


def import_bike_types(conn):
    print("Importazione bike_types...")
    df = pd.read_csv(assert_csv_exists("bike_types.csv"))

    cur = conn.cursor()
    try:
        for _, row in df.iterrows():
            cur.execute(
                """
                INSERT INTO bike_types (id, vehicle_image, name, description, form_factor,
                                      rider_capacity, propulsion_type, max_range, battery_capacity)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
                """,
                (
                    py_value(row["id"]),
                    py_value(row.get("vehicle_image")),
                    py_value(row.get("name")),
                    py_value(row.get("description")),
                    py_value(row.get("form_factor")),
                    py_value(row.get("rider_capacity")),
                    py_value(row.get("propulsion_type")),
                    py_value(row.get("max_range")),
                    py_value(row.get("battery_capacity")),
                ),
            )
        conn.commit()
        print(f"✓ {len(df)} tipi di bici importati")
    finally:
        cur.close()


def import_bikes(conn):
    print("Importazione bikes...")
    df = pd.read_csv(assert_csv_exists("bikes.csv"))

    cur = conn.cursor()
    try:
        for _, row in df.iterrows():
            cur.execute(
                """
                INSERT INTO bikes (id, bike_type_id, computer_id)
                VALUES (%s, %s, %s)
                ON CONFLICT (id) DO NOTHING
                """,
                (
                    py_value(row["id"]),
                    py_value(row.get("bike_type_id")),
                    py_value(row.get("computer_id")),
                ),
            )
        conn.commit()
        print(f"✓ {len(df)} biciclette importate")
    finally:
        cur.close()


def import_stations(conn):
    print("Importazione stations...")
    df = pd.read_csv(assert_csv_exists("stations.csv"))

    cur = conn.cursor()
    try:
        for _, row in df.iterrows():
            cur.execute(
                """
                INSERT INTO stations (id, city_id, name, app_number, terminal_type, place_type,
                                    bike_racks, special_racks, lon, lat)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
                """,
                (
                    py_value(row["id"]),
                    py_value(row["city_id"]),
                    py_value(row.get("name")),
                    py_value(row.get("app_number")),
                    py_value(row.get("terminal_type")),
                    py_value(row.get("place_type")),
                    py_value(row.get("bike_racks")),
                    py_value(row.get("special_racks")),
                    py_value(row.get("lon")),
                    py_value(row.get("lat")),
                ),
            )
        conn.commit()
        print(f"✓ {len(df)} stazioni importate")
    finally:
        cur.close()


# =============================================================================
# FK FIXERS (bikes/stations referenced by trips)
# =============================================================================

def ensure_bikes_for_trips(conn, trips_df: pd.DataFrame):
    cur = conn.cursor()
    try:
        trip_bike_ids = set(trips_df["bike_id"].dropna().astype(int).tolist())

        cur.execute("SELECT id FROM bikes")
        existing_bike_ids = {r[0] for r in cur.fetchall()}

        missing = sorted(trip_bike_ids - existing_bike_ids)
        if missing:
            print(f"  Trovate {len(missing)} bikes mancanti rispetto ai trips. Le inserisco...")
            for bid in missing:
                cur.execute(
                    """
                    INSERT INTO bikes (id, bike_type_id, computer_id)
                    VALUES (%s, NULL, NULL)
                    ON CONFLICT (id) DO NOTHING
                    """,
                    (int(bid),),
                )
            conn.commit()
            print("  ✓ bikes mancanti inserite")
        else:
            print("  ✓ Tutti i bike_id dei trips sono presenti in bikes")
    finally:
        cur.close()


def ensure_stations_for_trips(conn, trips_df: pd.DataFrame):
    cur = conn.cursor()
    try:
        pairs = []

        if "station_id_start" in trips_df.columns:
            tmp = trips_df[["station_id_start", "city_id"]].dropna(subset=["station_id_start"])
            for _, r in tmp.iterrows():
                pairs.append((int(r["station_id_start"]), int(r["city_id"])))

        if "station_id_end" in trips_df.columns:
            tmp = trips_df[["station_id_end", "city_id"]].dropna(subset=["station_id_end"])
            for _, r in tmp.iterrows():
                pairs.append((int(r["station_id_end"]), int(r["city_id"])))

        station_to_city = {}
        for sid, cid in pairs:
            if sid not in station_to_city:
                station_to_city[sid] = cid

        trip_station_ids = set(station_to_city.keys())

        cur.execute("SELECT id FROM stations")
        existing_station_ids = {r[0] for r in cur.fetchall()}

        missing = sorted(trip_station_ids - existing_station_ids)
        if missing:
            print(f"  Trovate {len(missing)} stations mancanti rispetto ai trips. Le inserisco...")
            for sid in missing:
                cid = station_to_city.get(sid)
                cur.execute(
                    """
                    INSERT INTO stations (id, city_id, name, app_number, terminal_type, place_type,
                                          bike_racks, special_racks, lon, lat)
                    VALUES (%s, %s, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL)
                    ON CONFLICT (id) DO NOTHING
                    """,
                    (int(sid), int(cid) if cid is not None else None),
                )
            conn.commit()
            print("  ✓ stations mancanti inserite")
        else:
            print("  ✓ Tutti i station_id dei trips sono presenti in stations")
    finally:
        cur.close()


# =============================================================================
# UTENTI (REALISTIC)
# =============================================================================

def generate_utenti(conn, n_utenti=300, seed=42):
    """
    Genera N utenti sintetici e ritorna la lista degli id creati.
    """
    print(f"Generazione utenti sintetici (n={n_utenti})...")

    from faker import Faker
    fake = Faker("it_IT")
    random.seed(seed)

    cur = conn.cursor()
    try:
        user_ids = []
        for i in range(n_utenti):
            nome = fake.first_name()
            cognome = fake.last_name()
            email = f"{nome.lower()}.{cognome.lower()}{i+1}@email.com"
            data_nascita = fake.date_of_birth(minimum_age=18, maximum_age=70)
            citta = fake.city()

            giorni_fa = random.randint(30, 1095)
            data_registrazione = pd.Timestamp.now() - pd.Timedelta(days=giorni_fa)

            tipo_abbonamento = random.choices(["Mensile", "Annuale"], weights=[40, 60])[0]
            stato = random.choices(["Attivo", "Sospeso"], weights=[92, 8])[0]

            cur.execute(
                """
                INSERT INTO utenti (bike_id, nome, cognome, email, data_nascita, citta,
                                  data_registrazione, tipo_abbonamento, stato)
                VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
                """,
                (
                    nome, cognome, email, data_nascita, citta,
                    data_registrazione, tipo_abbonamento, stato
                ),
            )
            user_ids.append(cur.fetchone()[0])

            if (i + 1) % 100 == 0:
                conn.commit()
                print(f"  Generati {i+1}/{n_utenti} utenti...")

        conn.commit()
        print(f"✓ {n_utenti} utenti generati")
        return user_ids
    finally:
        cur.close()


# =============================================================================
# TRIPS (with user_id)
# =============================================================================

def import_trips(conn, user_ids):
    print("Importazione trips...")
    df = pd.read_csv(assert_csv_exists("trips.csv"))

    # Fix FK: bikes e stations mancanti
    ensure_bikes_for_trips(conn, df)
    ensure_stations_for_trips(conn, df)

    # Sampler utenti realistico (pochi super-attivi)
    pick_user = make_heavy_user_sampler(user_ids, alpha=1.25)

    cur = conn.cursor()
    try:
        count = 0
        total = len(df)

        for _, row in df.iterrows():
            user_id = pick_user()

            cur.execute(
                """
                INSERT INTO trips (bike_id, city_id, time_start, lon_start, lat_start, lon_end, lat_end,
                                 station_id_start, station_id_end, battery_start, battery_end, duration, distance, user_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    py_value(row["bike_id"]),
                    py_value(row["city_id"]),
                    py_value(row["time_start"]),
                    py_value(row.get("lon_start")),
                    py_value(row.get("lat_start")),
                    py_value(row.get("lon_end")),
                    py_value(row.get("lat_end")),
                    py_value(row.get("station_id_start")),
                    py_value(row.get("station_id_end")),
                    py_value(row.get("battery_start")),
                    py_value(row.get("battery_end")),
                    py_value(row["duration"]),
                    py_value(row["distance"]),
                    user_id,
                ),
            )

            count += 1
            if count % 100 == 0:
                conn.commit()
                print(f"  Importati {count}/{total} trips...")

        conn.commit()
        print(f"✓ {total} trips importati")
    finally:
        cur.close()


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 70)
    print("IMPORT DATASET REALE EUROPEAN BIKE SHARING")
    print("=" * 70)

    if not DATA_DIR.exists():
        raise FileNotFoundError(f"DATA_DIR non esiste: {DATA_DIR}")

    conn = None
    try:
        conn = connect_db()
        print("✓ Connesso al database\n")

        import_cities(conn)
        import_bike_types(conn)
        import_bikes(conn)
        import_stations(conn)

        user_ids = generate_utenti(conn, n_utenti=300, seed=42)
        import_trips(conn, user_ids)

        print("\n" + "=" * 70)
        print("✓ IMPORT COMPLETATO CON SUCCESSO!")
        print("=" * 70)

    except Exception as e:
        print(f"\n✗ ERRORE: {e}")
        raise
    finally:
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    main()

