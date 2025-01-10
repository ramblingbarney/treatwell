resource "aws_s3_bucket" "movies_raw" {
  bucket = var.bucket_name
}

resource "aws_s3_bucket_public_access_block" "movies_raw" {
  bucket = aws_s3_bucket.movies_raw.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
