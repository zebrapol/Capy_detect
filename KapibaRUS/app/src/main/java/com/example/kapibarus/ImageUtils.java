package com.example.kapibarus;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;

import java.io.IOException;
import java.io.InputStream;

public class ImageUtils {
    public static Bitmap uriToBitmap(Context context, Uri imageUri) throws IOException {
        InputStream inputStream = context.getContentResolver().openInputStream(imageUri);
        return BitmapFactory.decodeStream(inputStream);
    }
}
