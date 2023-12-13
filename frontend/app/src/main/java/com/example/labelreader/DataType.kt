package com.example.labelreader

import com.google.gson.annotations.SerializedName

data class EncodedImageRequest(
    @SerializedName("encodedImageStr") val encodedImageStr: String
)
