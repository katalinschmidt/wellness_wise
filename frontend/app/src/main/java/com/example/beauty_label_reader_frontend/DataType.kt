package com.example.beauty_label_reader_frontend

import com.google.gson.annotations.SerializedName

data class EncodedImageRequest(
    @SerializedName("encodedImageStr") val encodedImageStr: String
)
