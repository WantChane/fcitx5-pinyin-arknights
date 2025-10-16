import os
import time
import click
from arkdicts.api.github import get_all_labels, delete_label, add_label
from arkdicts.constant import ALL_DICTS, REQUEST_DELAY


def generate_label_data(dict_names):
    return {f"incremental: {d}" for d in dict_names}


def batch_delete_labels(owner, repo, token, labels):
    for label in labels:
        success = delete_label(owner, repo, token, label)
        time.sleep(REQUEST_DELAY)
        if success:
            click.echo(click.style(f"Deleted label: {label}", fg="green"))
        else:
            click.echo(click.style(f"Failed to delete label: {label}", fg="red"))


def batch_add_labels(owner, repo, token, labels):
    for label in labels:
        success = add_label(owner, repo, token, label, "1BA784")
        time.sleep(REQUEST_DELAY)
        if success:
            click.echo(click.style(f"Added label: {label}", fg="green"))
        else:
            click.echo(click.style(f"Failed to add label: {label}", fg="red"))


@click.command("label")
def command():
    try:
        GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
    except KeyError:
        click.echo(
            click.style("GITHUB_TOKEN environment variable is required.", fg="red")
        )
        raise click.Abort()
    OWNER = "WantChane"
    REPO = "fcitx5-pinyin-arknights"

    data = get_all_labels(OWNER, REPO, GITHUB_TOKEN)
    if data:
        remote_labels = {
            item["name"] for item in data if item["name"].startswith("incremental: ")
        }
    else:
        click.echo(click.style("Failed to fetch labels from GitHub.", fg="red"))
        raise click.Abort()

    local_labels = generate_label_data(ALL_DICTS)

    delete_labels = remote_labels - local_labels
    if delete_labels:
        batch_delete_labels(OWNER, REPO, GITHUB_TOKEN, delete_labels)

    create_labels = local_labels - remote_labels
    if create_labels:
        batch_add_labels(OWNER, REPO, GITHUB_TOKEN, create_labels)

    click.echo(
        f"Deleted {len(delete_labels)} labels. \nCreated {len(create_labels)} labels. \nlabels Label synchronization completed."
    )
