# Cloud Resume Challenge — AWS

A fully serverless resume website built on AWS as part of the [Cloud Resume Challenge](https://cloudresumechallenge.dev). Live at **[paul-giff.com](https://paul-giff.com)**.

---

## Architecture

```
Browser → CloudFront (HTTPS) → S3 (HTML/CSS)
                                      ↓
                                JavaScript fetch
                                      ↓
                            API Gateway → Lambda → DynamoDB
```

Every push to `main` triggers a GitHub Actions workflow that syncs files to S3 and invalidates the CloudFront cache automatically.

---

## AWS Services Used

| Service | Purpose |
|---|---|
| S3 | Hosts the static HTML/CSS resume |
| CloudFront | CDN + HTTPS termination |
| Route 53 | Custom domain (paul-giff.com) |
| ACM | SSL/TLS certificate |
| API Gateway | HTTP endpoint for the visitor counter |
| Lambda | Python function that reads/writes visitor count |
| DynamoDB | Stores the visitor count |
| IAM | Permissions between services |
| GitHub Actions | CI/CD — auto-deploys on push to main |

---

## Project Structure

```
aws-s3-static-website/
├── index.html              # Resume page
├── style.css               # Styling
├── lambda_function.py      # Visitor counter Lambda function
├── test_lambda.py          # Unit tests for Lambda
├── .github/
│   └── workflows/
│       └── deploy.yml      # GitHub Actions CI/CD pipeline
├── docs/
│   └── notes.md            # Project notes
└── screenshots/            # Deployment screenshots
```

---

## CI/CD Pipeline

Every push to `main` automatically:
1. Configures AWS credentials via GitHub Secrets
2. Syncs all files to S3 (with exclusions for `.git`, `.github`, `README.md`, `docs/`)
3. Invalidates the CloudFront cache so visitors see the latest version immediately

---

## Visitor Counter

The visitor counter is fully serverless:

- **JavaScript** on the resume page calls the API Gateway endpoint on load
- **API Gateway** forwards the request to Lambda
- **Lambda** (Python) atomically increments the count in DynamoDB and returns it
- The count is displayed at the bottom of the resume page

---

## Tests

Unit tests for the Lambda function use Python's `unittest` with mocked DynamoDB:

```bash
python test_lambda.py
```

Tests cover:
- Returns HTTP 200 status code
- Returns `count` in the response body
- Returns correct CORS headers

---

## What I Learned

- IAM permissions are intentionally restrictive — every service needs explicit access grants
- CloudFront caches aggressively — always invalidate after updating S3 files
- CORS must be configured in API Gateway when the frontend and API are on different domains
- GitHub secret scanning is real — never put credentials anywhere near your code
- Serverless architecture is genuinely cheap for personal projects at this scale

---

## Blog Post

Full write-up of the build process, what broke, and what I learned:
[How I Built and Deployed My Resume on AWS](https://dev.to/p-giff)

---

## Author

**Paul Gifford** — DoD network & cybersecurity professional | TS Clearance | Cloud/AI pivot

- Website: [paul-giff.com](https://paul-giff.com)
- GitHub: [github.com/Paul-Gifford](https://github.com/Paul-Gifford)
- LinkedIn: [linkedin.com/in/paul-giff](https://linkedin.com/in/paul-giff)
