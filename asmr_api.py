"""
ASMR.ONE API 客户端
封装 asmr.one 网站后端接口，提供简洁的 Python API。

使用示例:
    from asmr_api import AsmrApi
    
    async with AsmrApi() as api:
        works = await api.get_works()
        results = await api.search("治愈")
"""

import httpx
from dataclasses import dataclass, field
from typing import Optional

BASE_URL = "https://api.asmr-200.com/api"


@dataclass
class AsmrApi:
    """ASMR.ONE API 客户端"""

    username: Optional[str] = None
    password: Optional[str] = None
    token: Optional[str] = field(default=None, repr=False)
    _client: Optional[httpx.AsyncClient] = field(default=None, repr=False, init=False)

    async def __aenter__(self):
        self._client = httpx.AsyncClient(
            base_url=BASE_URL,
            timeout=30.0,
            headers={"User-Agent": "AsmrApi/1.0"},
        )
        return self

    async def __aexit__(self, *exc):
        if self._client:
            await self._client.aclose()

    @property
    def _headers(self) -> dict:
        if self.token:
            return {"Authorization": f"Bearer {self.token}"}
        return {}

    # ── 认证 ──────────────────────────────────────────

    async def login(self) -> bool:
        """登录获取 token。需要先设置 username 和 password。"""
        if not self.username or not self.password:
            raise ValueError("需要提供 username 和 password")

        resp = await self._client.post(
            "/auth/me",
            json={"name": self.username, "password": self.password},
        )
        if resp.status_code == 200:
            data = resp.json()
            self.token = data.get("token")
            return True
        return False

    # ── 作品列表 ──────────────────────────────────────

    async def get_works(self, page: int = 1, order: str = "create_date",
                        sort: str = "desc", subtitle: int = 0) -> dict:
        """
        获取最新作品列表。
        
        参数:
            page: 页码，从1开始
            order: 排序字段 (create_date, release, dl_count, price, rate_average_2dp, review_count, id, random)
            sort: 排序方向 (asc, desc)
            subtitle: 是否仅字幕作品 (0=全部, 1=仅字幕)
        """
        resp = await self._client.get(
            "/works",
            params={"page": page, "order": order, "sort": sort, "subtitle": subtitle},
            headers=self._headers,
        )
        resp.raise_for_status()
        return resp.json()

    # ── 搜索 ──────────────────────────────────────────

    async def search(self, keyword: str, page: int = 1,
                     order: str = "release", sort: str = "desc",
                     subtitle: int = 0) -> dict:
        """
        搜索作品。

        参数:
            keyword: 搜索关键词
            page: 页码
            order: 排序字段
            sort: 排序方向
            subtitle: 是否仅字幕作品
        """
        resp = await self._client.get(
            f"/search/{keyword}",
            params={"page": page, "order": order, "sort": sort, "subtitle": subtitle},
            headers=self._headers,
        )
        resp.raise_for_status()
        return resp.json()

    # ── 单个作品 ──────────────────────────────────────

    async def get_work(self, work_id: int) -> dict:
        """获取单个作品详情。"""
        resp = await self._client.get(f"/work/{work_id}", headers=self._headers)
        resp.raise_for_status()
        return resp.json()

    # ── 音轨 ──────────────────────────────────────────

    async def get_tracks(self, work_id: int) -> list:
        """获取作品的音轨文件列表。"""
        resp = await self._client.get(f"/tracks/{work_id}", headers=self._headers)
        resp.raise_for_status()
        return resp.json()

    # ── 标签 ──────────────────────────────────────────

    async def get_tags(self) -> list:
        """获取所有标签（需要登录）。"""
        resp = await self._client.get("/tags", headers=self._headers)
        resp.raise_for_status()
        return resp.json()

    # ── 声优 ──────────────────────────────────────────

    async def get_vas(self) -> list:
        """获取所有声优列表（需要登录）。"""
        resp = await self._client.get("/vas", headers=self._headers)
        resp.raise_for_status()
        return resp.json()

    # ── 社团 ──────────────────────────────────────────

    async def get_circles(self) -> list:
        """获取所有社团列表（需要登录）。"""
        resp = await self._client.get("/circles", headers=self._headers)
        resp.raise_for_status()
        return resp.json()

    # ── 封面 URL ──────────────────────────────────────

    @staticmethod
    def cover_url(work_id: int, size: str = "main") -> str:
        """
        生成封面图 URL。

        参数:
            work_id: 作品 ID
            size: 图片尺寸 ('sam'=缩略图, '240x240'=小图, 'main'=原图)
        """
        return f"{BASE_URL}/cover/{work_id}.jpg?type={size}"


# ── 同步便捷函数 ─────────────────────────────────────

def search_sync(keyword: str, page: int = 1) -> dict:
    """同步搜索（便捷函数）。"""
    import asyncio
    async def _do():
        async with AsmrApi() as api:
            return await api.search(keyword, page=page)
    return asyncio.run(_do())


def get_works_sync(page: int = 1) -> dict:
    """同步获取作品列表（便捷函数）。"""
    import asyncio
    async def _do():
        async with AsmrApi() as api:
            return await api.get_works(page=page)
    return asyncio.run(_do())
