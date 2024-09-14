from flask import Flask, request, jsonify, render_template
import psycopg2
import b2sdk.v2

app = Flask(__name__)

# PostgreSQL Configuration
DB_HOST = 'localhost'
DB_NAME = 'pii_database'
DB_USER = 'soham'
DB_PASS = 'idfy_fraud'


B2_ACCOUNT_ID = '1af48fed9f34'
B2_APPLICATION_KEY = '003c91cec02d3184e64d26f87ce30797042bd05c6c'
B2_BUCKET_NAME = 'idfy-fraud-buster'


# PostgreSQL Connection
def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    return conn

# Backblaze B2 Connection
info = b2sdk.v2.InMemoryAccountInfo()
b2_api = b2sdk.v2.B2Api(info)
b2_api.authorize_account("production", B2_ACCOUNT_ID, B2_APPLICATION_KEY)
bucket = b2_api.get_bucket_by_name(B2_BUCKET_NAME)

@app.route('/database')
def fetch_database_data():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM pii_data;')
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify({'message': data})
@app.route('/cloud')
def fetch_cloud_data():
    try:
        # List files in the bucket
        files = bucket.ls()

        # List to store data from all files
        all_data = []

        for file_version, file_info in files:
            file_name = None  # Initialize file_name to avoid referencing before assignment
            try:
                # Fetch file info
                file_id = file_version.file_id
                file_name = file_version.file_name
                print(f"Attempting to download file: {file_name} (ID: {file_id})")
                
                # Download the file content
                file_content = bucket.download_file_by_id(file_id).read().decode('utf-8')
                
                # Log successful download
                print(f"Successfully downloaded file: {file_name}")
                
            except Exception as download_error:
                # Ensure file_name is not referenced before assignment, log more details for debugging
                error_message = f"Error downloading file {file_name if file_name else 'unknown'} (ID: {file_id if 'file_id' in locals() else 'unknown'}): {str(download_error)}"
                print(error_message)
                return jsonify({'error': error_message}), 500
            
            # Split the file content into lines
            lines = file_content.strip().split('\n')
            lines = [line.strip().strip('"') for line in lines]
            
            # Append the lines to all_data list
            all_data.extend(lines)
        
        return jsonify({'data': all_data})
    
    except Exception as e:
        error_message = f"Error fetching cloud data: {str(e)}"
        print(error_message)
        return jsonify({'error': error_message}), 500


@app.route('/fetch-data', methods=['POST'])
def fetch_data():
    try:
        source = request.json.get('source')
        if source == 'database':
            return fetch_database_data()
        elif source == 'cloud':
            return fetch_cloud_data()
        else:
            return jsonify({'error': 'Invalid source'}), 400
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500
@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
