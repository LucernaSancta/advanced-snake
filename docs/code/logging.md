# 🔧 Logs and logging
The logger is a custom tool made with the build-in `logging` python module and it provides a way to view, analize and store logs for better debugging and user experience.

## Customize Logging Levels
You can configure the logging level in the global configuration file under the `logs.level` flag:

```toml
[logs]
console_level="INFO"
file_level="DEBUG"
```

- `console_level` is for the console logs level.
- `file_level` is for the file logs level.

#### Available Logging Levels:

- **CRITICAL**: Critical errors that charash the program.
- **ERROR**: Errors that prevent normal operation.
- **WARNING**: Warnings about potential issues.
- **INFO**: Informational messages about normal operations.
- **DEBUG**: Detailed debugging information.

Each level includes logs of that level and all levels above it. For most use cases, we recommend using **INFO** or **DEBUG**.

## Using the Logger
You can access the logger directly through the `log` entity:

```python
log.warning('This is a warning message')
```

Alternatively, you can import it from the `logger.py` module:

```python
from logger import logger as log

log.info('This is an informational message')
```

By customizing the logging level and using the logger effectively, you can gain valuable insights into the application's behavior while debugging or monitoring.

---

⚠️ATTENTION⚠️ Code documentation is NOT regualary updated, this docs may be outdated