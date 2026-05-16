# Nexus404

## Description
Nexus404 is an autonomous multi-agent system built on .NET 9 and Python. It features a distributed architecture powered by NATS messaging, integrating various AI providers and capabilities including web scraping, document parsing, and Google Workspace integration.

## Architecture
- **Mira.API**: Main entry point and REST API.
- **Mira.Core**: Shared entities, domain models, and infrastructure abstractions.
- **Mira.Agents**: AI agent definitions and behaviors.
- **Mira.Missions**: Mission orchestration and lifecycle management.

## Integration & Capabilities
- **Messaging**: NATS messaging for high-performance communication between agents.
- **Data Storage**: PostgreSQL and SQLite via Entity Framework Core.
- **LLM Integration**: Support for OpenAI and Anthropic models.
- **Browser Automation**: PuppeteerSharp for headless browser control and scraping.
- **Document Processing**: PdfPig for PDF document analysis and HtmlAgilityPack for DOM manipulation.
- **Google Workspace**: Native integration with Google Auth, Calendar, Drive, and Gmail APIs.

## Installation

### Prerequisites
- .NET 9 SDK
- Python 3.11+
- PostgreSQL
- NATS Server

### Setup
1. Ensure the NATS server and PostgreSQL services are running on the system.
2. Configure the required environment variables:
   - `DB_CONNECTION_STRING`
   - `NATS_URL`
   - `OPENAI_ENDPOINT`
   - `ANTHROPIC_ENDPOINT`

3. Restore .NET dependencies:
   dotnet restore

4. Build the project:
   dotnet build --configuration Release

5. Run the main API service:
   dotnet run --project Mira.API --configuration Release
[WARNING] --raw-output is enabled. Model output is not sanitized and may contain harmful ANSI sequences (e.g. for phishing or command injection). Use --accept-raw-output-risk to suppress this warning.