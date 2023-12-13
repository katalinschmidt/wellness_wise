package com.example.labelreader

import retrofit2.Call
import retrofit2.http.Body
import retrofit2.http.POST

interface ApiService {
    @POST("/upload")
    fun uploadPhoto(@Body requestBody: EncodedImageRequest): Call<Map<String, Any>>
}