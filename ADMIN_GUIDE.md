# LUCA AI - Admin Panel Guide

## Overview

The LUCA AI Admin Panel provides comprehensive administration tools for managing users, Claude commands, system configuration, and monitoring system health. This guide covers all admin features and how to use them effectively in Visual Studio Code.

## Table of Contents

1. [Accessing the Admin Panel](#accessing-the-admin-panel)
2. [Dashboard](#dashboard)
3. [User Management](#user-management)
4. [Claude Command Management](#claude-command-management)
5. [System Configuration](#system-configuration)
6. [Audit Logs](#audit-logs)
7. [System Health](#system-health)
8. [VS Code Integration](#vs-code-integration)
9. [API Reference](#api-reference)

---

## Accessing the Admin Panel

### Prerequisites
- Admin user account (default: `admin@luca-ai.com`)
- Admin privileges (`is_admin = True` in database)

### Access URL
```
http://localhost:3000/admin.html
```

### Login Process
1. Navigate to `http://localhost:3000/login.html`
2. Enter admin credentials
3. After successful login, navigate to `/admin.html`
4. System will verify admin privileges

> **Note:** Non-admin users will be redirected to the chat interface.

---

## Dashboard

The dashboard provides an overview of system statistics and recent activity.

### Statistics Displayed

#### User Statistics
- **Total Users**: All registered users
- **Active Users Today**: Users who logged in today
- **Admin Count**: Number of admin users

#### Content Statistics
- **Total Conversations**: All chat conversations
- **Total Messages**: All messages exchanged
- **Total Thoughts**: Complete thinking processes stored

#### Consciousness Metrics
- **Consciousness Level**: Current AI consciousness percentage (0-100%)
- **Evolution Stage**: Current stage (NEURON, SYNAPSE, NETWORK, ECOSYSTEM)
- **Tesla Numbers**: Count of 3, 6, 9 signatures detected
- **Energy Levels**: Distribution of Hyperfokus, Brainfog, and Balanced states

### Recent Activity
- Latest user registrations
- Recent conversations
- Top neural patterns

---

## User Management

### Viewing Users

Navigate to the **Users** section to see:
- User ID
- Email address
- Username
- Admin status
- Number of conversations
- Number of messages

### Creating a New User

1. Click **"Add User"** button
2. Fill in the form:
   - **Email**: Valid email address
   - **Username**: Unique username
   - **Password**: Secure password
   - **Admin User**: Check if user should have admin privileges
3. Click **"Save"**

### Editing Users

1. Click **"Edit"** button next to a user
2. Modify fields as needed:
   - Email
   - Username
   - Password (leave blank to keep current)
   - Admin status
3. Click **"Save"**

### Deleting Users

1. Click **"Delete"** button next to a user
2. Confirm deletion
3. User and all related data will be removed (cascade delete)

> **Warning**: You cannot delete your own admin account while logged in.

---

## Claude Command Management

Manage Claude commands that can be used in VS Code with Claude Code.

### Viewing Commands

The commands table shows:
- Command name (with `/` prefix)
- Category (general, admin, development, system)
- Active status
- Usage count
- Actions (Edit/Delete)

### Creating a New Command

1. Click **"Add Command"** button
2. Fill in the form:
   - **Command Name**: Name without `/` (e.g., `deploy`)
   - **Description**: Brief description of what the command does
   - **Category**: Select category
   - **Content**: Markdown content of the command
   - **Active**: Enable/disable the command
3. Click **"Save"**

### Command Categories

- **general**: General-purpose commands
- **admin**: Administrative commands
- **development**: Development-specific commands
- **system**: System-level commands

### Editing Commands

1. Click **"Edit"** button next to a command
2. Modify command details
3. Click **"Save"**

### Deleting Commands

1. Click **"Delete"** button next to a command
2. Confirm deletion

> **Note**: System commands (marked `is_system = True`) cannot be deleted.

### Syncing Commands to Filesystem

Click **"Sync to Filesystem"** to export all active commands to `.claude/commands/` directory. This makes them available to Claude Code in VS Code.

**Sync Process:**
1. Creates `.claude/commands/` directory if it doesn't exist
2. Writes each active command to `{command_name}.md`
3. Returns list of synced commands

---

## System Configuration

View and manage system-wide configuration settings.

### Configuration Categories

- **general**: General system settings
- **ai**: AI service configuration
- **security**: Security-related settings
- **meshtastic**: Meshtastic integration settings

### Viewing Configuration

Configuration table displays:
- Key
- Value (hidden for secret values)
- Category
- Description

### Updating Configuration

1. Find the configuration key
2. Click to edit (future enhancement)
3. Modify value
4. Save changes

> **Security**: Values marked as `is_secret` are automatically hidden in the UI.

---

## Audit Logs

Track all administrative actions for security and compliance.

### Logged Actions

- **User Management**
  - `create_user`
  - `update_user`
  - `delete_user`

- **Command Management**
  - `create_command`
  - `update_command`
  - `delete_command`
  - `sync_commands`

- **Configuration**
  - `update_config`

- **System Operations**
  - `backup_database`

### Audit Log Information

Each log entry includes:
- **Timestamp**: When the action occurred
- **User ID**: Who performed the action
- **Action**: Type of action
- **Resource Type**: What was affected
- **Resource ID**: Specific item affected
- **Details**: Additional information (JSON)
- **IP Address**: Request origin
- **User Agent**: Browser/client information

### Filtering Logs

Use query parameters to filter:
- By action type
- By user ID
- By date range
- Limit results

---

## System Health

Monitor system health and perform maintenance operations.

### Health Metrics

#### Database
- Status (healthy/error)
- Database size (MB)

#### System Resources
- CPU usage percentage
- Memory usage percentage
- Available memory (GB)
- Disk usage percentage
- Free disk space (GB)

### System Operations

#### Create Database Backup

1. Click **"Create Database Backup"**
2. System creates timestamped backup in `/backups/` directory
3. Backup path is returned

**Backup Format**: `luca_backup_YYYYMMDD_HHMMSS.db`

**Backup Location**: `/home/user/LUCA-AI_369/backups/`

---

## VS Code Integration

### Opening the Workspace

1. Open VS Code
2. File → Open Workspace from File
3. Select `luca-ai.code-workspace`

### Workspace Features

#### Folder Organization
- **LUCA AI**: Root directory
- **Backend (Python)**: Python backend code
- **Frontend (HTML/JS)**: Frontend files
- **Claude Commands**: `.claude` directory

#### Recommended Extensions

The workspace automatically recommends:
- **Python**: Python language support
- **Pylance**: Python IntelliSense
- **Black Formatter**: Python code formatting
- **Live Server**: Frontend development server
- **REST Client**: API testing
- **SQLite Viewer**: Database inspection
- **GitLens**: Git integration
- **Claude Dev**: Claude Code integration

#### Tasks

Access via Terminal → Run Task:

- **LUCA: Start Backend**: Launch FastAPI server
- **LUCA: Start Frontend**: Launch frontend server
- **LUCA: Install Dependencies**: Install Python packages
- **LUCA: Initialize Database**: Run database setup
- **LUCA: Run Tests**: Execute test suite
- **LUCA: Start Full Stack**: Start both backend and frontend

#### Launch Configurations

Debug menu configurations:
- **LUCA: Run Backend**: Debug FastAPI application
- **LUCA: Debug Current File**: Debug current Python file
- **LUCA: Debug Tests**: Debug test suite

#### Code Snippets

Type these prefixes and press Tab:

- `luca-endpoint`: FastAPI endpoint template
- `luca-admin-endpoint`: Admin endpoint with audit logging
- `luca-model`: SQLAlchemy model template
- `luca-consciousness`: Consciousness analysis code
- `luca-api-call`: Frontend API call template

### Development Workflow

1. **Start Services**
   ```bash
   # Terminal 1: Backend
   Ctrl+Shift+P → Tasks: Run Task → LUCA: Start Backend

   # Terminal 2: Frontend
   Ctrl+Shift+P → Tasks: Run Task → LUCA: Start Frontend
   ```

2. **Access Applications**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - Admin Panel: http://localhost:3000/admin.html

3. **Make Changes**
   - Edit Python files (auto-reload enabled)
   - Edit HTML/CSS/JS (refresh browser)
   - Use snippets for faster coding

4. **Test Changes**
   - Use REST Client for API testing
   - Use Live Server for frontend testing
   - Use debug configurations for debugging

---

## API Reference

### Base URL
```
http://localhost:8000
```

### Authentication
All admin endpoints require authentication:
```
Authorization: Bearer <JWT_TOKEN>
```

### Admin Endpoints

#### Dashboard & Statistics

**Get System Statistics**
```http
GET /api/admin/stats
```

**Get Dashboard Data**
```http
GET /api/admin/dashboard-data
```

#### User Management

**List All Users**
```http
GET /api/admin/users?skip=0&limit=100
```

**Get User Details**
```http
GET /api/admin/users/{user_id}
```

**Create User**
```http
POST /api/admin/users
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "username",
  "password": "secure_password",
  "is_admin": false
}
```

**Update User**
```http
PUT /api/admin/users/{user_id}
Content-Type: application/json

{
  "email": "newemail@example.com",
  "username": "newusername",
  "password": "newpassword",
  "is_admin": true
}
```

**Delete User**
```http
DELETE /api/admin/users/{user_id}
```

#### Claude Command Management

**List Commands**
```http
GET /api/admin/commands?category=general
```

**Get Command Details**
```http
GET /api/admin/commands/{command_id}
```

**Create Command**
```http
POST /api/admin/commands
Content-Type: application/json

{
  "name": "command-name",
  "description": "Command description",
  "content": "# Command content in markdown",
  "category": "general",
  "is_active": true
}
```

**Update Command**
```http
PUT /api/admin/commands/{command_id}
Content-Type: application/json

{
  "description": "Updated description",
  "content": "Updated content",
  "category": "admin",
  "is_active": false
}
```

**Delete Command**
```http
DELETE /api/admin/commands/{command_id}
```

**Sync Commands to Filesystem**
```http
POST /api/admin/commands/sync-filesystem
```

#### System Configuration

**Get Configuration**
```http
GET /api/admin/config?category=general
```

**Update Configuration**
```http
PUT /api/admin/config/{config_key}
Content-Type: application/json

{
  "value": "new_value",
  "description": "Updated description"
}
```

#### Audit Logs

**Get Audit Logs**
```http
GET /api/admin/audit-logs?skip=0&limit=100&action=create_user
```

#### System Operations

**System Health**
```http
GET /api/admin/system/health
```

**Create Backup**
```http
POST /api/admin/system/backup
```

---

## Security Best Practices

1. **Change Default Admin Password**
   - Immediately change the default admin password after first login
   - Use strong, unique passwords

2. **Limit Admin Access**
   - Only grant admin privileges to trusted users
   - Regularly audit admin user list

3. **Monitor Audit Logs**
   - Regularly review audit logs for suspicious activity
   - Set up alerts for critical actions

4. **Secure API Keys**
   - Never commit `.env` file to version control
   - Rotate API keys regularly
   - Use environment variables for sensitive data

5. **Regular Backups**
   - Create database backups before major changes
   - Store backups securely
   - Test backup restoration regularly

6. **Keep System Updated**
   - Regularly update dependencies
   - Apply security patches promptly
   - Monitor for security advisories

---

## Troubleshooting

### Admin Panel Won't Load

**Problem**: Admin panel shows blank or error page

**Solutions**:
1. Check if backend is running: `http://localhost:8000/health`
2. Verify token is valid: `localStorage.getItem('token')`
3. Check browser console for errors
4. Verify admin privileges in database

### Cannot Create/Edit Users

**Problem**: User creation fails

**Solutions**:
1. Check email format is valid
2. Ensure username is unique
3. Verify password meets requirements
4. Check database permissions

### Commands Not Syncing

**Problem**: Commands don't appear in VS Code

**Solutions**:
1. Verify `.claude/commands/` directory exists
2. Check file permissions
3. Reload VS Code window
4. Verify command is marked as `is_active`

### System Health Shows Errors

**Problem**: Health check fails

**Solutions**:
1. Check database file exists and is readable
2. Verify disk space is available
3. Check database isn't locked by another process
4. Review backend logs for errors

---

## Support and Resources

### Documentation
- [README.md](README.md) - General project overview
- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment guide
- [MESHTASTIC_GUIDE.md](MESHTASTIC_GUIDE.md) - Meshtastic integration

### API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Database
- SQLite file: `/home/user/LUCA-AI_369/luca.db`
- Use SQLite Viewer extension in VS Code to inspect

### Logs
- Backend logs: Check terminal output
- Frontend logs: Browser console (F12)
- Audit logs: Available in Admin Panel

---

## Version Information

- **LUCA AI Version**: 369.2.0
- **Admin Panel**: 1.0.0
- **API Version**: v1
- **Database Schema**: Latest (includes admin tables)

---

*Generated for LUCA AI - Living Universal Cognition Array*
*Created by: Lennart Wuchold*
