# Building the Google Classroom API Bridge

To allow Faraday to automatically pull your coursework, assignments, and lecture notes directly from your IISER Google Classroom, we need to create an "API Bridge." 

Google highly secures student data, so you cannot just feed it a username and password. Instead, you have to create an **OAuth2 Client App** on Google Cloud. This will give you a `credentials.json` file. 

Once you have that file, Antigravity can write a Python script that uses it to log into your classroom securely and pull the data.

## Step-by-Step Guide to getting `credentials.json`

### Step 1: Create a Google Cloud Project
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Log in with your primary Google account (preferably the one connected to your Classroom, though not strictly required if you add it as a test user later).
3. In the top-left dropdown, click **New Project**. Name it something like `Faraday Classroom Bridge` and click **Create**.

### Step 2: Enable the Classroom API
1. Using the left-hand navigation menu, go to **APIs & Services** -> **Library**.
2. Search for **Google Classroom API**.
3. Click on it and hit the blue **Enable** button.

### Step 3: Configure the OAuth Consent Screen
*This tells Google exactly what data the script is allowed to look at.*
1. Go to **APIs & Services** -> **OAuth consent screen**.
2. Choose **External** (unless you are using a G-Suite/Workspace admin account, then choose Internal). Click **Create**.
3. Fill out the required fields:
   - **App Name:** `Faraday`
   - **User Support Email:** Select your email.
   - **Developer Contact:** Enter your email.
4. Click **Save and Continue**.
5. On the **Scopes** screen, click **Add or Remove Scopes**. Search for and add:
   - `.../auth/classroom.courses.readonly`
   - `.../auth/classroom.coursework.me.readonly`
6. Click **Save and Continue**.
7. On the **Test Users** screen, click **Add Users** and manually type in the **exact email address you use for Google Classroom** (e.g., your @iisertvm.ac.in email). *This is crucial, or the script will be blocked.*

### Step 4: Download your Key (`credentials.json`)
1. Go to **APIs & Services** -> **Credentials**.
2. Click the **+ Create Credentials** button at the top and select **OAuth client ID**.
3. Under **Application type**, select **Desktop app** (since you will run this locally on your PC). Name it "Faraday Script".
4. Click **Create**.
5. A popup will appear. Click the **Download JSON** button.
6. Rename this downloaded file exactly to: **`credentials.json`**.
7. Move `credentials.json` directly into this folder: `c:\Users\msaur\OneDrive\Desktop\Obsidian\obsidian\Faraday\03 - Data Lake\course_data\`

---

## What Happens Next?

Once you have placed `credentials.json` in the folder, just tell Antigravity:
> **"I have my credentials.json. Build the Classroom sync script."**

I will then write the exact Python tool that will authenticate you safely and download all your course materials, deadlines, and grades into your wiki!
