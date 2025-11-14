# Firebase Setup for Multi-User Collaboration

This guide will help you set up Firebase Firestore to enable multi-user collaboration on trip planning.

## Why Firebase?

Firebase allows multiple people to share and edit the same trip using a unique trip code (e.g., "Ohboy"). Without Firebase, the app will work locally only on your device.

## Setup Steps

### 1. Create a Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click **"Add project"** or **"Create a project"**
3. Enter a project name (e.g., "Disney Trip Planner")
4. Click through the setup wizard (you can disable Google Analytics if you want)

### 2. Enable Firestore Database

1. In your Firebase project, click **"Firestore Database"** in the left sidebar
2. Click **"Create database"**
3. Choose **"Start in production mode"** (we'll set up rules next)
4. Select a Cloud Firestore location (choose one closest to you)
5. Click **"Enable"**

### 3. Configure Firestore Security Rules

1. Click on the **"Rules"** tab in Firestore
2. Replace the rules with the following to allow anyone with a trip code to read/write:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Allow anyone to read and write trips
    // Security is based on knowing the trip code
    match /trips/{tripCode} {
      allow read, write: if true;
    }
  }
}
```

3. Click **"Publish"**

> **Note:** This setup allows anyone with the trip code to access the trip data. The trip code acts as the password. Keep your trip code private and only share with trusted travel companions.

### 4. Generate Service Account Credentials

1. Click the ⚙️ **Settings** icon → **Project settings**
2. Go to the **"Service accounts"** tab
3. Click **"Generate new private key"**
4. Click **"Generate key"** - a JSON file will download
5. **IMPORTANT:** Keep this file secure! Don't commit it to Git.

### 5. Configure Credentials

#### For Local Development:

1. Open the downloaded JSON file
2. Copy the entire contents
3. Set it as an environment variable:

**On Mac/Linux:**
```bash
export FIREBASE_CREDENTIALS='paste-your-json-here'
```

**On Windows (Command Prompt):**
```cmd
set FIREBASE_CREDENTIALS=paste-your-json-here
```

**Or add to your `.env` file:**
```
FIREBASE_CREDENTIALS={"type":"service_account","project_id":"...","private_key_id":"..."}
```

#### For Streamlit Cloud Deployment:

1. Go to your Streamlit Cloud app settings
2. Click on **"Secrets"**
3. Add the following (replace with your actual Firebase credentials):

```toml
[firebase]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\nYour-Private-Key\n-----END PRIVATE KEY-----\n"
client_email = "your-service-account@your-project.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "your-cert-url"
```

4. Save the secrets

### 6. Install Dependencies

Make sure firebase-admin is installed:

```bash
pip install firebase-admin>=6.0.0
```

Or install all requirements:

```bash
pip install -r requirements.txt
```

## Testing Multi-User Access

### Test Scenario:

1. **Person 1** opens the app and creates a trip with code "Ohboy"
2. **Person 1** fills in trip details and creates a checklist
3. **Person 2** opens the app (on a different device or browser)
4. **Person 2** clicks "Join Existing Trip" and enters "Ohboy"
5. **Person 2** should see all the trip details and checklist that Person 1 created
6. Both people can now edit the trip and see each other's changes (after refresh)

## Troubleshooting

### "Cloud sync not configured" Warning

This means Firebase credentials weren't found. Check:
- Environment variable `FIREBASE_CREDENTIALS` is set correctly
- Streamlit secrets are configured correctly
- The JSON format is valid

### "Trip code not found" Error

This means the trip doesn't exist in Firebase yet. Make sure:
- Someone created the trip first using "Create New Trip"
- Firebase is properly configured
- The trip code is spelled exactly the same way

### Local-Only Mode

If Firebase is not configured, the app will still work but will save data locally only. You won't be able to share trips with others until Firebase is set up.

## Cost

Firebase has a **free tier** (Spark plan) that includes:
- 1 GB storage
- 50,000 reads/day
- 20,000 writes/day
- 20,000 deletes/day

This is **more than enough** for personal trip planning with 4-6 people!

## Security Note

The trip code acts as the password. Anyone with the code can:
- View all trip details
- Edit the trip
- Add/remove checklist items
- Chat with the AI assistant

**Keep your trip code private** and only share with trusted travel companions.
