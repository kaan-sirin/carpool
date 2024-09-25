import click
import json


def match_trip(paths_list, start, end):
    matched_trips = []

    for path in paths_list:
        if start in path and end in path:
            if path.index(start) < path.index(end):
                matched_trips.append(path)

    return matched_trips


@click.command()
@click.option(
    "--paths",
    type=click.Path(exists=True),
    required=True,
    help="Path to a JSON file with a list of paths (each path is a list of integers).",
)
@click.option(
    "--from-area-id",
    required=True,
    type=int,
    help="The start destination (an integer).",
)
@click.option(
    "--to-area-id", required=True, type=int, help="The end destination (an integer)."
)
def main(paths, from_area_id, to_area_id):
    try:
        with open(paths, "r") as json_file:
            paths_list = json.load(json_file)
    except (json.JSONDecodeError, FileNotFoundError):
        click.echo(
            "Invalid JSON file or file not found. Please provide a valid path to a JSON file."
        )
        return

    # Validate that paths are a list of lists of integers
    if not all(
        isinstance(path, list) and all(isinstance(i, int) for i in path)
        for path in paths_list
    ):
        click.echo("Invalid paths format. Paths must be a list of lists of integers.")
        return

    matched_trips = match_trip(paths_list, from_area_id, to_area_id)

    if matched_trips:
        click.echo(
            f"Matching trips found for trip from {from_area_id} to {to_area_id}:"
        )
        for matched_trip in matched_trips:
            click.echo(f"Matched Path: {matched_trip}")
    else:
        click.echo(
            f"No matching trips found for trip from {from_area_id} to {to_area_id}."
        )


if __name__ == "__main__":
    main()
