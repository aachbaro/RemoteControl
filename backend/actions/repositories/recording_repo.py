from actions.models import Recording


def get_singleton() -> Recording:
    obj, _ = Recording.objects.get_or_create(
        id=1,
        defaults={"is_recording": False, "started_at": None},
    )
    return obj


def save(rec: Recording, *, update_fields=None) -> None:
    if update_fields:
        rec.save(update_fields=update_fields)
    else:
        rec.save()