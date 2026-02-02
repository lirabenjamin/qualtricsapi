---
name: Feature Request - Response Management
about: Add support for retrieving, exporting, and managing survey responses
title: '[FEATURE] Add Response Management and Export Support'
labels: enhancement, v0.4.0
assignees: ''
---

## Feature Request: Response Management and Export

### Description
Add functionality to retrieve, export, and manage survey responses. This enables programmatic access to response data for analysis, reporting, and integration with other systems.

### Use Cases

1. **Data Retrieval**: Download survey responses for analysis
2. **Real-time Monitoring**: Check response counts and completion rates
3. **Data Export**: Export responses in various formats (CSV, JSON, SPSS)
4. **Data Cleaning**: Delete test responses or duplicates
5. **Integration**: Feed response data into other systems automatically
6. **Reporting**: Generate automated reports from response data
7. **Quality Control**: Monitor response quality and identify issues

### Proposed API

```python
# Get response count
count = api.get_response_count(survey_id)
print(f"Total responses: {count}")

# List responses (with pagination)
responses = api.list_responses(
    survey_id,
    start_date="2024-01-01",
    end_date="2024-12-31",
    status="Complete",  # or "Incomplete", "All"
    limit=100,
    offset=0
)

# Get single response
response = api.get_response(survey_id, response_id)
print(response['values'])  # Response data

# Export responses
export_id = api.create_response_export(
    survey_id,
    format="csv",  # or "json", "spss", "xml"
    start_date="2024-01-01",
    end_date=None,
    include_incomplete=False,
    use_labels=True,  # Use choice labels instead of codes
    columns=[  # Optional: specific columns
        "QID1", "QID2", "QID3"
    ]
)

# Check export status
status = api.get_export_status(survey_id, export_id)
print(f"Export status: {status['status']}")  # "in progress", "complete", "failed"

# Download export when complete
if status['status'] == 'complete':
    file_path = api.download_export(
        survey_id,
        export_id,
        save_to="responses.csv"
    )
    print(f"Downloaded to: {file_path}")

# Convenience method: export and download in one call
api.export_responses(
    survey_id,
    format="csv",
    save_to="responses.csv",
    wait_for_completion=True  # Waits until export ready
)

# Delete response (e.g., test responses)
api.delete_response(survey_id, response_id)

# Delete multiple responses
api.delete_responses(survey_id, response_ids=["R_xxx", "R_yyy"])

# Update response (for data correction)
api.update_response(
    survey_id,
    response_id="R_xxx",
    values={
        "QID1": "1",  # Update answer to question 1
        "QID2": "Updated text"
    }
)

# Get response summary statistics
stats = api.get_response_statistics(survey_id)
print(f"Complete: {stats['complete']}")
print(f"Incomplete: {stats['incomplete']}")
print(f"Average time: {stats['avg_completion_time']} seconds")

# Get responses with filters
responses = api.get_responses_filtered(
    survey_id,
    filters={
        "QID1": "1",  # Only responses where QID1 = 1
        "embedded_data.department": "Engineering"
    }
)
```

### Technical Details

**Qualtrics API Endpoints:**
- `GET /surveys/{surveyId}/responses` - List responses
- `GET /surveys/{surveyId}/responses/{responseId}` - Get single response
- `POST /surveys/{surveyId}/export-responses` - Create export
- `GET /surveys/{surveyId}/export-responses/{exportProgressId}` - Check export status
- `GET /surveys/{surveyId}/export-responses/{exportProgressId}/file` - Download export file
- `DELETE /surveys/{surveyId}/responses/{responseId}` - Delete response
- `PUT /surveys/{surveyId}/responses/{responseId}` - Update response

**Export Formats Supported:**
- CSV (Comma-separated values)
- JSON (JavaScript Object Notation)
- SPSS (Statistical Package for Social Sciences)
- XML (Extensible Markup Language)
- TSV (Tab-separated values)

**Response Object Structure:**
```json
{
  "responseId": "R_xxx",
  "values": {
    "QID1": "1",
    "QID2": "Response text",
    "QID3_1": "5"
  },
  "labels": {
    "QID1": "Choice 1",
    "QID2": "Response text",
    "QID3_1": "Strongly Agree"
  },
  "displayedFields": ["QID1", "QID2", "QID3"],
  "displayedValues": {...},
  "responseMetadata": {
    "startDate": "2024-01-01T10:00:00Z",
    "endDate": "2024-01-01T10:15:00Z",
    "status": "Complete",
    "ipAddress": "192.168.1.1",
    "progress": 100,
    "duration": 900,
    "finished": true,
    "recordedDate": "2024-01-01T10:15:00Z"
  }
}
```

**Implementation Requirements:**

1. New module: `qualtrics_sdk/core/responses.py` with `ResponseMixin`
2. Methods for:
   - Listing and retrieving responses
   - Creating and managing exports
   - Downloading export files
   - Deleting responses
   - Updating responses (if needed)
   - Getting statistics
3. Export manager with polling/waiting logic
4. Response data parser for different formats
5. Update `QualtricsAPI` class to include `ResponseMixin`
6. Documentation in `docs/RESPONSE_MANAGEMENT_GUIDE.md`
7. Example scripts:
   - `examples/export_responses.py`
   - `examples/response_monitoring.py`
   - `examples/data_cleaning.py`

### Export Flow

The export process is asynchronous:

1. Create export request → get `exportProgressId`
2. Poll status endpoint until `status == "complete"`
3. Download file using exportProgressId
4. Optionally delete export after download

Implementation should handle:
- Polling with backoff (check every 5s, then 10s, then 30s)
- Timeout after reasonable period (e.g., 10 minutes)
- Error handling for failed exports
- Automatic cleanup of completed exports

### Response Data Handling

```python
# Helper: Convert responses to pandas DataFrame
import pandas as pd

responses = api.get_all_responses(survey_id)
df = pd.DataFrame([r['values'] for r in responses])

# Helper: Get responses as iterator for large datasets
for response in api.iter_responses(survey_id, batch_size=100):
    process_response(response)

# Helper: Response filtering and transformation
responses = api.get_responses(
    survey_id,
    transform=lambda r: {
        'id': r['responseId'],
        'completed': r['responseMetadata']['finished'],
        'duration': r['responseMetadata']['duration'],
        **r['values']
    }
)
```

### Documentation Needs

- Complete guide on response management
- Examples for common scenarios:
  - Basic export workflow
  - Real-time response monitoring
  - Automated reporting pipeline
  - Data cleaning procedures
  - Integration with pandas/analysis tools
- Best practices:
  - Handling large datasets
  - Export format selection
  - Data privacy considerations
  - Rate limiting and API quotas
- Troubleshooting common issues

### Testing Requirements

- [ ] Get response count
- [ ] List responses with pagination
- [ ] Get single response by ID
- [ ] Create CSV export
- [ ] Create JSON export
- [ ] Check export status
- [ ] Download completed export
- [ ] Test export with date filters
- [ ] Test export with status filters
- [ ] Delete single response
- [ ] Delete multiple responses
- [ ] Update response values
- [ ] Get response statistics
- [ ] Test with large response set (>1000 responses)
- [ ] Test export timeout handling
- [ ] Test malformed response data

### Related Features

- Survey creation and management (responses come from surveys)
- Embedded data (appears in response data)
- Data analysis tools (responses feed into analysis)
- Distribution management (distributions generate responses)

### Priority

**High** - Response data is the primary output of surveys; accessing it programmatically is essential

### Version Target

v0.4.0 (as specified in ROADMAP.md)

### Resources

- [Qualtrics Response API Documentation](https://api.qualtrics.com/ZG9jOjg3NzY3MA-getting-survey-responses-via-the-new-export-ap-is)
- [Qualtrics Export API Guide](https://api.qualtrics.com/6b00592b9c013-create-response-export)
- [Response Data Format Documentation](https://www.qualtrics.com/support/survey-platform/data-and-analysis-module/data/download-data/understanding-your-dataset/)

### Acceptance Criteria

- [ ] Can retrieve response count
- [ ] Can list responses with filters
- [ ] Can get individual response
- [ ] Can create export in multiple formats (CSV, JSON, SPSS)
- [ ] Export process handles polling automatically
- [ ] Can download completed export
- [ ] Can delete responses
- [ ] Can update responses (if API supports)
- [ ] Export with date range filtering works
- [ ] Export with completion status filtering works
- [ ] All methods have proper error handling
- [ ] Timeout handling for long exports
- [ ] Support for large datasets (pagination)
- [ ] Comprehensive documentation with examples
- [ ] Working example scripts for common workflows
- [ ] Integration examples with pandas/analysis tools
- [ ] Tests pass successfully

---

**Additional Notes:**

Response management is critical for survey workflows. The export API is asynchronous, so implementation needs robust polling and timeout handling. Consider rate limits - the Qualtrics API may limit how many exports can be created in a time period.

For large surveys with many responses, pagination and streaming are important. Consider adding helpers for common data analysis workflows (e.g., direct export to pandas DataFrame).

Security note: Response data may contain PII. Documentation should emphasize data privacy best practices and compliance considerations (GDPR, etc.).
