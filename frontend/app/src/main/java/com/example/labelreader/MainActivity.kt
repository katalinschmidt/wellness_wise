package com.example.labelreader

import android.content.ContentResolver
import android.net.Uri
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Base64
import android.util.Log
import android.widget.Button
import android.widget.Toast
import androidx.activity.result.contract.ActivityResultContracts

import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import java.io.ByteArrayOutputStream
import java.io.InputStream


class MainActivity : AppCompatActivity() {

    /**
     * Called when the activity is first created.
     *
     * An Android app typically consists of multiple screens or views, each represented by an Activity, and
     * this method is part of the Android Activity lifecycle. It is invoked when the activity is created,
     * i.e. when the app is launched or when a user navigates to a specific screen.
     *
     * @param savedInstanceState A Bundle containing the saved state of the activity, if available.
     */
    override fun onCreate(savedInstanceState: Bundle?) {
        // Initialize the primary user interface and
        // set the content view to the layout defined in 'activity_main.xml'
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // Initialize UI elements
        val uploadPhotoBtn = findViewById<Button>(R.id.upload_photo_btn)

        // Set click listener for UI elements
        uploadPhotoBtn.setOnClickListener {
            // FIXME: Rename and/or refactor pickImageLauncher
            pickImageLauncher.launch("image/*")
        }
    }

    private fun showToast(message: String) {
        Toast.makeText(this, message, Toast.LENGTH_SHORT).show()
    }

    private fun executeRequest(call: Call<Map<String, Any>>) {
        call.enqueue(object : Callback<Map<String, Any>> {
            override fun onResponse(call: Call<Map<String, Any>>, response: Response<Map<String, Any>>) {
                if (response.isSuccessful) {
                    val responseData = response.body()
                    if (responseData != null) {
                        Log.i("apiCall", "Successful API call, found data")
                    } else {
                        Log.i("apiCall", "Successful API call, empty data")
                    }
                } else {
                    Log.e("apiCall", "Unsuccessful API call")
                    Log.e("apiCall", "Status Code: ${response.code()}")
                    Log.e("apiCall", "Error Message: ${response.errorBody()}")
                }
            }

            override fun onFailure(call: Call<Map<String, Any>>, t: Throwable) {
                Log.e("apiCall", "Failure calling API: $t")
            }
        })
    }

    private val pickImageLauncher =
        registerForActivityResult(ActivityResultContracts.GetContent()) { selectedImageUri: Uri? ->
            if (selectedImageUri != null)  {
                Log.i("pickImageLauncher", "Successfully retrieved URI: $selectedImageUri")

                // Encode image
                val contentResolver: ContentResolver = applicationContext.contentResolver
                val encodedImage = convertImageUriToBase64(contentResolver, selectedImageUri)
                if (encodedImage != null) {
                    Log.i("pickImageLauncher", "Successfully converted to base64: $encodedImage")

                    // Convert to data type & POST to backend
                    val requestBody = EncodedImageRequest(encodedImage)
                    val call = RetrofitInstance.api.uploadPhoto(requestBody)
                    executeRequest(call)

                } else {
                    Log.e("pickImageLauncher", "Failed to convert to base64")
                }

            } else {
                Log.e("imageUpload", "Failed to find URI")
            }
        }

    private fun convertImageUriToBase64(contentResolver: ContentResolver, imageUri: Uri): String? {
        try {
            var inputStream: InputStream? = null
            inputStream = contentResolver.openInputStream(imageUri)
            val imageBytes = inputStream?.let { readBytesFromInputStream(it) }
            val encodedImageBytes = Base64.encode(imageBytes, Base64.DEFAULT)
            return String(encodedImageBytes)
        } catch (e: Exception) {
            e.printStackTrace()
        }
        return null
    }

    private fun readBytesFromInputStream(inputStream: InputStream): ByteArray {
        val buffer = ByteArrayOutputStream()
        val data = ByteArray(1024)
        var length: Int
        while (inputStream.read(data).also { length = it } != -1) {
            buffer.write(data, 0, length)
        }
        buffer.flush()
        return buffer.toByteArray()
    }

}
