
def test_pagination(webapp, page_size):
    object_ids = [obj["id"] for obj in webapp.get_all_paged(page_size)]
    assert object_ids == list(range(1, webapp.num_objects + 1))

def test_pagination_different_renderer(webapp, page_size):
    assert webapp.get_all_paged(page_size, path="objects_different_renderer") == [{"id_value": i} for i in range(1, webapp.num_objects + 1)]
