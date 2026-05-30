#!/bin/bash
# Script to create an Android application with a WebView pointing to app.html
# and automatically generate the APK.

APP_NAME="MyWebApp"
PACKAGE_NAME="com.example.mywebapp"
PROJECT_DIR="$APP_NAME"
BUILD_TYPE=${1:-debug}   # debug or release

mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR" || exit 1

cat > settings.gradle <<EOF
rootProject.name = '$APP_NAME'
include ':app'
EOF

cat > build.gradle <<EOF
plugins {
    id 'com.android.application' version '8.2.0' apply false
}
EOF

mkdir -p app/src/main/java/com/example/mywebapp
mkdir -p app/src/main/assets
mkdir -p app/src/main/res/layout

cat > app/build.gradle <<EOF
plugins {
    id 'com.android.application'
}

android {
    namespace '$PACKAGE_NAME'
    compileSdk 34

    defaultConfig {
        applicationId '$PACKAGE_NAME'
        minSdk 21
        targetSdk 34
        versionCode 1
        versionName '1.0'
    }

    buildTypes {
        release {
            minifyEnabled false
        }
    }
}
EOF

cat > app/src/main/AndroidManifest.xml <<EOF
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <application
        android:label="$APP_NAME"
        android:theme="@android:style/Theme.DeviceDefault.Light.NoActionBar">
        <activity android:name=".MainActivity" android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
EOF

cat > app/src/main/res/layout/activity_main.xml <<EOF
<?xml version="1.0" encoding="utf-8"?>
<WebView xmlns:android="http://schemas.android.com/apk/res/android"
    android:id="@+id/webView"
    android:layout_width="match_parent"
    android:layout_height="match_parent" />
EOF

cat > app/src/main/java/com/example/mywebapp/MainActivity.java <<EOF
package com.example.mywebapp;

import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebView;

public class MainActivity extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        WebView webView = findViewById(R.id.webView);
        webView.getSettings().setJavaScriptEnabled(true);
        webView.loadUrl("file:///android_asset/app.html");
    }
}
EOF

cat > app/src/main/assets/app.html <<EOF
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>App HTML</title>
</head>
<body>
    <h1>Android App with WebView</h1>
    <p>Content loaded from app.html</p>
</body>
</html>
EOF

cat > gradlew <<EOF
#!/bin/bash
./gradle wrapper
./gradlew assembleDebug
EOF

chmod +x gradlew

echo "Project created in: $PROJECT_DIR"

if [ "$BUILD_TYPE" = "release" ]; then
    ./gradlew assembleRelease
    echo "Release APK generated at: app/build/outputs/apk/release/app-release.apk"
else
    ./gradlew assembleDebug
    echo "Debug APK generated at: app/build/outputs/apk/debug/app-debug.apk"
fi

echo "APK generated successfully."
