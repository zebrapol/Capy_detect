package com.example.kapibarus;

import android.content.Context;
import android.content.res.AssetFileDescriptor;
import android.graphics.Bitmap;
import android.net.Uri;

import org.tensorflow.lite.Interpreter;
import java.io.ByteArrayOutputStream;
import java.io.FileInputStream;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.channels.FileChannel;

public class Model {
    private final Interpreter interpreter;
    private static final int IMAGE_SIZE = 224;

    public Model(Context context) throws IOException {
        // Загрузка модели из assets
        ByteBuffer modelBuffer = loadModelFile(context);
        Interpreter.Options options = new Interpreter.Options();
        options.setNumThreads(4);
        interpreter = new Interpreter(modelBuffer, options);
    }

    private ByteBuffer loadModelFile(Context context) throws IOException {
        AssetFileDescriptor fileDescriptor = context.getAssets().openFd("model.tflite");
        FileInputStream inputStream = new FileInputStream(fileDescriptor.getFileDescriptor());
        FileChannel fileChannel = inputStream.getChannel();
        long startOffset = fileDescriptor.getStartOffset();
        long declaredLength = fileDescriptor.getDeclaredLength();
        return fileChannel.map(FileChannel.MapMode.READ_ONLY, startOffset, declaredLength);
    }


    private ByteBuffer convertBitmapToByteBuffer(Bitmap bitmap) {
        ByteBuffer byteBuffer = ByteBuffer.allocateDirect(4 * IMAGE_SIZE * IMAGE_SIZE * 3); // 4 байта на float, 3 канала (RGB)
        byteBuffer.order(ByteOrder.nativeOrder());
        int[] pixels = new int[IMAGE_SIZE * IMAGE_SIZE];
        bitmap.getPixels(pixels, 0, IMAGE_SIZE, 0, 0, IMAGE_SIZE, IMAGE_SIZE);

        for (int pixel : pixels) {
            float r = ((pixel >> 16) & 0xFF) / 255.0f;
            float g = ((pixel >> 8) & 0xFF) / 255.0f;
            float b = (pixel & 0xFF) / 255.0f;
            byteBuffer.putFloat(r);
            byteBuffer.putFloat(g);
            byteBuffer.putFloat(b);
        }
        return byteBuffer;
    }


    public String predictFromUri(Context context, Uri imageUri) throws IOException {

        Bitmap originalBitmap = ImageUtils.uriToBitmap(context, imageUri);


        Bitmap resizedBitmap = Bitmap.createScaledBitmap(originalBitmap, IMAGE_SIZE, IMAGE_SIZE, true);
        ByteBuffer inputBuffer = convertBitmapToByteBuffer(resizedBitmap);


        float[][] output = new float[1][1];
        interpreter.run(inputBuffer, output);


        return convertClassToText((int) output[0][0]);
    }

    //Взято в качестве примера, позже будет исправлено
    private String convertClassToText(int classIndex) {
        String[] labels = {"Кошка", "Собака", "Птица"};
        return (classIndex >= 0 && classIndex < labels.length) ? labels[classIndex] : "Неизвестно";
    }

    public void close() {
        interpreter.close();
    }
}