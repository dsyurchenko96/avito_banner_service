from hashlib import sha256

from sqlalchemy.orm import Session

from app.models.banner import BannerPostRequest
from app.models.tables import Banner, Feature, Tag

admin_token = sha256(b"admin").digest().hex()
user_token = sha256(b"user").digest().hex()

error_details = {
    400: {"detail": "Некорректные данные"},
    401: {"detail": "Пользователь не авторизован"},
    403: {"detail": "Пользователь не имеет доступа"},
    404: {"detail": "Баннер не найден"},
}


def insert_manual_data(db: Session, num_cycles=1, add_banner=True, is_active=True):
    for _ in range(num_cycles):
        feature = Feature(description="new feature")
        tag = Tag()
        tag2 = Tag()
        db.add_all([feature, tag, tag2])
        db.commit()
        if add_banner:
            insert_banner(db, feature.id, [tag, tag2], is_active)


def insert_banner(db: Session, feature_id: int, tags: list[Tag], is_active=True):
    banner = Banner(
        feature_id=feature_id,
        content={"title": "some_title", "text": "some_text", "url": "some_url"},
        is_active=is_active,
    )
    banner.associated_tags = tags
    db.add(banner)
    db.commit()


class TestGetUserBanner:
    def test_invalid_request_no_feature_and_tag(self, test_client, db_session):
        response = test_client.get("/user_banner", params={"token": user_token})
        assert response.status_code == 400
        assert response.json() == error_details[400]

    def test_invalid_request_feature_no_tag(self, test_client, db_session):
        response = test_client.get(
            "/user_banner", params={"token": user_token, "feature_id": 1}
        )
        assert response.status_code == 400
        assert response.json() == error_details[400]

    def test_invalid_request_tag_no_feature(self, test_client, db_session):
        response = test_client.get(
            "/user_banner", params={"token": user_token, "tag_id": 1}
        )
        assert response.status_code == 400
        assert response.json() == error_details[400]

    def test_invalid_token(self, test_client, db_session):
        response = test_client.get(
            "/user_banner", params={"token": "", "feature_id": 1, "tag_id": 1}
        )
        assert response.status_code == 401
        assert response.json() == error_details[401]

    def test_is_not_active_banner(self, test_client, db_session):
        insert_manual_data(db_session, add_banner=True, is_active=False)

        response = test_client.get(
            "/user_banner", params={"token": user_token, "feature_id": 1, "tag_id": 1}
        )
        assert response.status_code == 404
        assert response.json() == error_details[404]

    def test_not_found_banner(self, test_client, db_session):
        insert_manual_data(db_session, add_banner=False)

        response = test_client.get(
            "/user_banner", params={"token": user_token, "feature_id": 1, "tag_id": 1}
        )
        assert response.status_code == 404
        assert response.json() == error_details[404]

    def test_valid_request_admin_token(self, test_client, db_session):
        insert_manual_data(db_session)

        response = test_client.get(
            "/user_banner", params={"token": admin_token, "feature_id": 1, "tag_id": 1}
        )
        assert response.status_code == 200
        assert response.json() == {
            "content": {"url": "some_url", "text": "some_text", "title": "some_title"}
        }

    def test_valid_request(self, test_client, db_session):
        insert_manual_data(db_session)

        response = test_client.get(
            "/user_banner", params={"token": user_token, "feature_id": 1, "tag_id": 1}
        )
        assert response.status_code == 200
        assert response.json() == {
            "content": {"url": "some_url", "text": "some_text", "title": "some_title"}
        }


class TestGetAdminBanners:
    def test_empty_db(self, test_client, db_session):
        response = test_client.get("/banner", params={"token": admin_token})
        assert response.status_code == 404
        assert response.json() == error_details[404]

    def test_invalid_user_token(self, test_client, db_session):
        response = test_client.get("/banner", params={"token": user_token})
        assert response.status_code == 403
        assert response.json() == error_details[403]

    def test_invalid_other_token(self, test_client, db_session):
        response = test_client.get("/banner", params={"token": ""})
        assert response.status_code == 401
        assert response.json() == error_details[401]

    def test_one_valid_no_filter(self, test_client, db_session):
        insert_manual_data(db_session)

        response = test_client.get("/banner", params={"token": admin_token})
        assert response.status_code == 200
        assert response.json()[0]["id"] == 1

    def test_multiple_valid_no_filter(self, test_client, db_session):
        insert_manual_data(db_session, num_cycles=2)

        response = test_client.get("/banner", params={"token": admin_token})
        assert response.status_code == 200
        assert len(response.json()) == 2
        assert response.json()[0]["id"] == 1
        assert response.json()[1]["id"] == 2

    def test_one_valid_with_feature_filter(self, test_client, db_session):
        insert_manual_data(db_session, num_cycles=5)

        params = {"token": admin_token, "feature_id": 1}
        response = test_client.get("/banner", params=params)
        assert response.status_code == 200
        assert response.json()[0]["id"] == 1

    def test_multiple_valid_with_tag_feature_filter(self, test_client, db_session):
        feature1 = Feature()
        feature2 = Feature()
        tag1 = Tag()
        tag2 = Tag()
        tag3 = Tag()
        db_session.add_all([feature1, feature2, tag1, tag2, tag3])
        db_session.commit()
        insert_banner(db_session, feature1.id, [tag1, tag2])
        insert_banner(db_session, feature2.id, [tag2, tag3])

        params_feature_tag = {"token": admin_token, "feature_id": 1, "tag_id": 2}
        response_feature_tag = test_client.get("/banner", params=params_feature_tag)
        assert response_feature_tag.status_code == 200
        assert len(response_feature_tag.json()) == 1
        assert response_feature_tag.json()[0]["id"] == 1

        params_tag = {"token": admin_token, "tag_id": 2}
        response_tag = test_client.get("/banner", params=params_tag)
        assert response_tag.status_code == 200
        assert len(response_tag.json()) == 2
        assert response_tag.json()[0]["id"] == 1
        assert response_tag.json()[1]["id"] == 2

    def test_offset(self, test_client, db_session):
        insert_manual_data(db_session, num_cycles=5)

        params = {"token": admin_token, "offset": 2}
        response = test_client.get("/banner", params=params)
        assert response.status_code == 200
        assert len(response.json()) == 3
        assert response.json()[0]["id"] == 3
        assert response.json()[1]["id"] == 4
        assert response.json()[2]["id"] == 5

    def test_limit(self, test_client, db_session):
        insert_manual_data(db_session, num_cycles=5)

        params = {"token": admin_token, "limit": 2}
        response = test_client.get("/banner", params=params)
        assert response.status_code == 200
        assert len(response.json()) == 2
        assert response.json()[0]["id"] == 1
        assert response.json()[1]["id"] == 2

    def test_offset_and_limit(self, test_client, db_session):
        insert_manual_data(db_session, num_cycles=5)

        params = {"token": admin_token, "offset": 2, "limit": 2}
        response = test_client.get("/banner", params=params)
        assert response.status_code == 200
        assert len(response.json()) == 2
        assert response.json()[0]["id"] == 3
        assert response.json()[1]["id"] == 4

    def test_invalid_offset(self, test_client, db_session):
        insert_manual_data(db_session, num_cycles=5)

        params = {"token": admin_token, "offset": -1}
        response = test_client.get("/banner", params=params)
        assert response.status_code == 400
        assert response.json() == error_details[400]


class TestPostBanners:
    default_request = BannerPostRequest(
        feature_id=1,
        content={"title": "some_title", "text": "some_text", "url": "some_url"},
        is_active=True,
        tag_ids=[1, 2],
    )

    def test_invalid_user_token(self, test_client, db_session):
        response = test_client.post(
            "/banner",
            json=self.default_request.model_dump(),
            params={"token": user_token},
        )
        assert response.status_code == 403
        assert response.json() == error_details[403]

    def test_invalid_other_token(self, test_client, db_session):
        response = test_client.post(
            "/banner",
            json=self.default_request.model_dump(),
            params={"token": "definitely invalid token"},
        )
        assert response.status_code == 401
        assert response.json() == error_details[401]

    def test_already_exists(self, test_client, db_session):
        insert_manual_data(db_session, add_banner=True)
        response = test_client.post(
            "/banner",
            json=self.default_request.model_dump(),
            params={"token": admin_token},
        )
        assert response.status_code == 400
        assert response.json() == error_details[400]

    def test_invalid_request(self, test_client, db_session):
        insert_manual_data(db_session, add_banner=False)
        response = test_client.post(
            "/banner",
            json={"title": "some_title", "text": "some_text", "url": "some_url"},
            params={"token": admin_token},
        )
        assert response.status_code == 400
        assert response.json() == error_details[400]

    def test_invalid_feature_id(self, test_client, db_session):
        insert_manual_data(db_session, add_banner=False)
        request = self.default_request.model_dump()
        request["feature_id"] = 5
        response = test_client.post(
            "/banner",
            json=request,
            params={"token": admin_token},
        )
        assert response.status_code == 400
        assert response.json() == error_details[400]

    def test_valid(self, test_client, db_session):
        insert_manual_data(db_session, add_banner=False)
        response = test_client.post(
            "/banner",
            json=self.default_request.model_dump(),
            params={"token": admin_token},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["id"] == 1


class TestPatchBanners:
    def test_invalid_user_token(self, test_client, db_session):
        response = test_client.patch(
            "/banner/1",
            json={"content": {"text": "new_text"}},
            params={"token": user_token},
        )
        assert response.status_code == 403
        assert response.json() == error_details[403]

    def test_invalid_other_token(self, test_client, db_session):
        response = test_client.patch(
            "/banner/1",
            json={"content": {"text": "new_text"}},
            params={"token": "that's not a token"},
        )
        assert response.status_code == 401
        assert response.json() == error_details[401]

    def test_invalid_endpoint(self, test_client, db_session):
        response = test_client.patch(
            "/banner/abanner",
            json={"title": "some_title", "text": "some_text", "url": "some_url"},
            params={"token": admin_token},
        )
        assert response.status_code == 400
        assert response.json() == error_details[400]

    def test_invalid_body(self, test_client, db_session):
        insert_manual_data(db_session, add_banner=True)
        response = test_client.patch(
            "/banner/1",
            json={"some_key": "some_value"},
            params={"token": admin_token},
        )
        assert response.status_code == 400
        assert response.json() == error_details[400]

    def test_nonexistent_banner_empty_db(self, test_client, db_session):
        response = test_client.patch(
            "/banner/1",
            json={"content": {"text": "new_text"}},
            params={"token": admin_token},
        )
        assert response.status_code == 404
        assert response.json() == error_details[404]

    def test_nonexistent_banner_nonempty_db(self, test_client, db_session):
        insert_manual_data(db_session, add_banner=True)
        response = test_client.patch(
            "/banner/2",
            json={"content": {"text": "new_text"}},
            params={"token": admin_token},
        )
        assert response.status_code == 404
        assert response.json() == error_details[404]

    def test_valid(self, test_client, db_session):
        insert_manual_data(db_session, add_banner=True)
        response = test_client.patch(
            "/banner/1",
            json={"content": {"text": "new_text"}},
            params={"token": admin_token},
        )
        assert response.status_code == 200
        updated_response = test_client.get(
            "/banner/", params={"token": admin_token, "feature_id": 1, "tag_id": 1}
        )
        assert updated_response.json()[0]["content"]["text"] == "new_text"


class TestDeleteBanners:
    def test_invalid_user_token(self, test_client, db_session):
        response = test_client.delete(
            "/banner/1",
            params={"token": user_token},
        )
        assert response.status_code == 403
        assert response.json() == error_details[403]

    def test_invalid_other_token(self, test_client, db_session):
        response = test_client.delete(
            "/banner/1",
            params={"token": "that's not a token"},
        )
        assert response.status_code == 401
        assert response.json() == error_details[401]

    def test_invalid_endpoint(self, test_client, db_session):
        response = test_client.delete(
            "/banner/somerandomendpoint",
            params={"token": admin_token},
        )
        assert response.status_code == 400
        assert response.json() == error_details[400]

    def test_invalid_banner_id(self, test_client, db_session):
        response = test_client.delete(
            "/banner/-2",
            params={"token": admin_token},
        )
        assert response.status_code == 400
        assert response.json() == error_details[400]

    def test_nonexistent_banner_empty_db(self, test_client, db_session):
        response = test_client.delete(
            "/banner/1",
            params={"token": admin_token},
        )
        assert response.status_code == 404
        assert response.json() == error_details[404]

    def test_nonexistent_banner_nonempty_db(self, test_client, db_session):
        insert_manual_data(db_session, add_banner=True)
        response = test_client.delete(
            "/banner/2",
            params={"token": admin_token},
        )
        assert response.status_code == 404
        assert response.json() == error_details[404]

    def test_valid(self, test_client, db_session):
        insert_manual_data(db_session, add_banner=True)
        before_response = test_client.get(
            "/banner/", params={"token": admin_token, "feature_id": 1, "tag_id": 1}
        )
        assert before_response.status_code == 200
        response = test_client.delete(
            "/banner/1",
            params={"token": admin_token},
        )
        assert response.status_code == 204
        after_response = test_client.get(
            "/banner/", params={"token": admin_token, "feature_id": 1, "tag_id": 1}
        )
        assert after_response.status_code == 404
