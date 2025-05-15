def is_instructor(user):
    """Check if the user is an instructor."""
    return user.is_authenticated and (hasattr(user, 'courses_teaching') or hasattr(user, 'instructor_profile')) 