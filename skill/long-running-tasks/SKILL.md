---
name: long-running-tasks
description: Handle tasks that may exceed tool timeouts (model training, large builds, data processing).
---

# Long-Running Tasks

## Use when
- Running tasks that may take more than 10 minutes (model quantization, training, large builds)
- Starting processes that should continue even if the connection drops
- Monitoring background jobs and reporting progress

## Don't use when
- The task completes quickly and fits within the normal tool timeout window.
- The task must be interactive (requires continuous prompts or TTY input).

## Outputs
- Log files (e.g., `task.log`, `build.log`) should be saved in `artifacts/` when possible.
- Final outputs should be written to `artifacts/` for easy retrieval.

## Templates or Examples
- Use the command patterns in the “Commands” and “Examples” sections as templates.

## Strategy

For any task that might exceed the Bash tool timeout (10 minutes):

1. **Run in background** with output logging
2. **Return immediately** to confirm the task started
3. **Check periodically** and report progress
4. **Confirm completion** when done

## Commands

### Start a long-running task

```bash
# Use nohup to persist after session ends, redirect all output to log
nohup <command> > task.log 2>&1 &
echo "Task started with PID $!"
```

### Check if task is still running

```bash
# Check by process name
pgrep -f "<command_pattern>" && echo "Still running" || echo "Completed"

# Or check the log for completion indicators
tail -20 task.log
```

### Monitor progress

```bash
# Watch log file for updates
tail -f task.log  # (use with timeout or Ctrl+C)

# Or get last N lines
tail -50 task.log
```

## Examples

### Model Quantization

```bash
# Start quantization in background
nohup python quantize.py --model GLM-4.7-flash --format NVFP4 > quantize.log 2>&1 &
echo "Quantization started. Check quantize.log for progress."
```

Then periodically:
```bash
tail -30 quantize.log
pgrep -f "quantize.py" && echo "Still running..." || echo "Process completed!"
```

### Large Build

```bash
# Start build in background
nohup cargo build --release > build.log 2>&1 &
echo "Build started with PID $!"
```

Check progress:
```bash
tail -20 build.log
```

### Data Processing Pipeline

```bash
# Start pipeline
nohup ./process_data.sh input/ output/ > pipeline.log 2>&1 &

# Check progress (if script outputs progress)
grep -E "Progress|Completed|Error" pipeline.log | tail -10
```

## Best Practices

1. **Always use `nohup`** - Ensures task survives if connection drops
2. **Redirect both stdout and stderr** - Use `> file.log 2>&1`
3. **Save the PID** - `echo $!` right after starting
4. **Check periodically** - Every 5-10 minutes for long tasks
5. **Look for completion markers** - grep for "done", "error", "completed"
6. **Clean up** - Remove log files after confirming success

## Reporting to User

When starting a long task, tell the user:
- What command was started
- Where logs are saved
- How to check progress manually
- Estimated completion time (if known)

When checking progress, report:
- Current status (running/completed/failed)
- Recent log output (last 10-20 lines)
- Any errors or warnings seen

When task completes:
- Confirm success or failure
- Summarize results
- Clean up temporary files if appropriate
