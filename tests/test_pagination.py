
def test_pagination(webapp):
    object_ids = [obj["id"] for i in range(1, (webapp.num_objects / 2) + 2) for obj in webapp.get_page(2, i)]
    assert object_ids == list(range(1, webapp.num_objects + 1))
