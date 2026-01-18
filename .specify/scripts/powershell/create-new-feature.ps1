param(
    [Parameter(Mandatory=$true)]$Json,
    [Parameter(Mandatory=$false)]$Number,
    [Parameter(Mandatory=$false)]$ShortName,
    [Parameter(ValueFromRemainingArguments=$true)]$FeatureDescription
)

# Create the specs directory if it doesn't exist
if (!(Test-Path "specs")) {
    New-Item -ItemType Directory -Path "specs" -Force
}

# Create the feature directory
$featureDir = "specs/$Number-$ShortName"
if (!(Test-Path $featureDir)) {
    New-Item -ItemType Directory -Path $featureDir -Force
}

# Create the spec file
$specFile = "$featureDir/spec.md"
if (!(Test-Path $specFile)) {
    # Create a basic template
    @"
# Specification: $ShortName

## Overview

[Overview of the feature]

## User Scenarios & Testing

[User scenarios and testing requirements]

## Functional Requirements

[Detailed functional requirements]

## Success Criteria

[Measurable success criteria]

## Key Entities

[Key data entities if applicable]

## Dependencies & Assumptions

[Any dependencies or assumptions]

## Non-Goals

[Things explicitly not included]

"@ | Out-File -FilePath $specFile -Encoding UTF8
}

# Output the results as JSON
$result = @{
    BRANCH_NAME = "$Number-$ShortName"
    SPEC_FILE = $specFile
    FEATURE_DIR = $featureDir
} | ConvertTo-Json

Write-Output $result
