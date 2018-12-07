from pathlib import Path


# Make arguments readable to other components
def expandargs(args):
    if args.MAPFILE is not None:
        args.MAPFILE = str(Path(args.MAPFILE).expanduser().resolve())
    if args.tileset is not None:
        args.tileset = str(Path(args.tileset).expanduser().resolve())
    if args.output is not None:
        args.output = str(Path(args.output).expanduser().resolve())

    return args
