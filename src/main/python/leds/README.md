# Threads Intro

## Sequential blinks in a single thread

### Usage

```bash
$ ./non_threaded.py 
```

### CLI Options

| Option         | Description                                        | Default |
|:---------------|----------------------------------------------------|---------|
| -p, --pause    | Blink pause (secs)                                 | 0.25    |

## Overlapping, random blinks in multiple threads

### Usage

```bash
$ ./threaded.py 
```

### CLI Options

| Option         | Description                                        | Default |
|:---------------|----------------------------------------------------|---------|
| -p, --pause    | Blink pause (secs)                                 | 0.5     |

## Non-overlapping, random blinks in multiple threads

### Usage

```bash
$ ./with_lock.py 
```

### CLI Options

| Option         | Description                                        | Default |
|:---------------|----------------------------------------------------|---------|
| -p, --pause    | Blink pause (secs)                                 | 0.05    |
| -f, --fair     | Blink fairly                                       | false   |

## Sequential blinks in multiple threads

### Usage

```bash
$ ./with_event.py 
```

### CLI Options

| Option         | Description                                        | Default |
|:---------------|----------------------------------------------------|---------|
| -p, --pause    | Blink pause (secs)                                 | 0.05    |
| -r, --reverse  | Reverse blink direction                            | false   |

