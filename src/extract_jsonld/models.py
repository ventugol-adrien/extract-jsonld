from pydantic import BaseModel


class JobPosting(BaseModel):
    title: str
    description: str
    datePosted: str
    company: str
    company_domain: str
    location: str
    platform: str

    @classmethod
    def convert(cls, data: dict):
        raise NotImplementedError(f"{cls.__name__} must implement the convert method.")

    @classmethod
    def from_dict(cls, data: dict, platform: str = ""):
        if platform == "ashby":
            return AshbyJobPosting.convert(data)

    @classmethod
    def from_dict_array(cls, data_list: list, platform: str = ""):
        return [cls.from_dict(data, platform) for data in data_list]


class AshbyJobPosting(JobPosting):
    @classmethod
    def convert(cls, data: dict):
        if not data:
            return None
        return cls(
            title=data.get("title", ""),
            description=data.get("description", ""),
            datePosted=data.get("datePosted", ""),
            company=data.get("company", ""),
            company_domain=data.get("hiringOrganization", {}).get("sameAs", ""),
            location=data.get("location", ""),
            platform="ashby",
        )
