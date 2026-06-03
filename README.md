# Secure Academic Research & Portfolio Repository

## Project Overview
A digital portfolio generator where university faculty can upload publications, datasets, and credentials. It allows peer reviewers to access specific files securely while keeping sensitive raw data locked from the general public.

## Technical Requirements

- **Data & UI**
  - Cloudinary integration for large PDF/Dataset uploads.
  - Inline formsets to add multiple co-authors to a single research paper upload.

- **Security**
  - Strict object-level permissions using `OwnerOrManagerMixin`, ensuring researchers can only edit their own portfolios.
  - Rate-limiting on document download endpoints.

- **API**
  - Django REST Framework endpoints for external citation engines.
  - Premium/Reviewer JWT tokens reveal full PDF links, while basic requests only return abstracts.

## Notes
This repository is designed as a secure academic portfolio system with a focus on resource access control, researcher ownership, and external API integration.

## Cloudinary Setup
1. Open `.env` in the project root.
2. Set your Cloudinary credentials:
   - `CLOUDINARY_CLOUD_NAME`
   - `CLOUDINARY_API_KEY`
   - `CLOUDINARY_API_SECRET`
3. Use `USE_CLOUD_STORAGE=True` to enable Cloudinary uploads.
4. Restart the Django server.

The app is configured to store uploaded files in Cloudinary using `RawMediaCloudinaryStorage` when `USE_CLOUD_STORAGE` is enabled.
Uploaded files are saved in the Cloudinary folder named `uploaded files`.
