from django.http import JsonResponse
from django.views.generic import View

from search.models import RestaurantType
from rrsite.util.json import CustomResponseJson

from elasticsearch_dsl import Search
from datetime import datetime


class SearchSuggest(View):
    def get(self, request):
        key_words = request.GET.get('s', '')
        if not key_words:
            return JsonResponse(CustomResponseJson('关键词不能为空', code=0))

        data = list()
        s = Search.from_dict
        s = s.suggest(name='suggestion', text=key_words, completion=dict(
            field='suggest',
            fuzzy=dict(
                fuzziness=0
            ),
            size=10
        ))
        suggestions = s.execute()

        for match in suggestions.suggest.suggestion[0].options:
            restaurant_id = match['_id']
            name = match['_source']['name']
            address = match['_source']['address']
            if restaurant_id is not None and name is not None:
                data.append(dict(id=restaurant_id, name=name, address=address))
        return JsonResponse(CustomResponseJson(msg='查询建议成功', code=1, data=data))


class SearchView(View):
    def get(self, request):
        # 获取关键词参数
        key_words = request.GET.get('s', None)
        city = request.GET.get('city', None)
        lat = request.GET.get('lat', None)
        lon = request.GET.get('lon', None)
        price_range = request.GET.get('pricerange', None)
        query_dict = {
            'query': {
                'bool': {
                    'filter': [],
                    'must': []
                }
            },
            'from': 0,
            'size': 10,
            '_source': ['name', 'address', 'city', 'state', 'postal_code', 'neighborhood', 'stars', 'review_count',
                        'location', 'is_open', 'attribute.RestaurantsPriceRange2'],
            'highlight': {
                'fields': {
                    'name': {},
                    'address': {}
                },
                'pre_tags': '<span>',
                'post_tags': '</span>'
            }
        }
        # 获取页码
        page = request.GET.get('p', 1)
        try:
            page = int(page)
        except ValueError:
            page = 1
        if key_words:
            query_dict['query']['bool']['must'].append(
                dict(multi_match={
                    'query': key_words,
                    'fields': ['name^5', 'address']
                }))

        if city:
            city = str(city).replace('-', ' ')
            query_dict['query']['bool']['filter'].append(dict(term={'city': city}))

        if price_range:
            query_dict['query']['bool']['filter'].append(
                dict(nested={
                        'path': 'attribute',
                        'score_mode': 'avg',
                        'query': {
                            'bool': {
                                'must': [
                                    {'match': {'attribute.RestaurantsPriceRange2': price_range}}
                                ]
                            }
                        }
                    }))

        try:
            if lat and lon:
                lat = float(lat)
                lon = float(lon)
                query_dict['query']['bool']['filter'].append(
                    dict(geo_distance={
                        'location': [lon, lat],
                        'distance': '20km'
                    }))
        except ValueError:
            return JsonResponse(CustomResponseJson('位置信息错误', code=0))
        # # 高亮关键词，用于填充模板
        # s = s.highlight_options(pre_tags='<em>', post_tags='</em>')
        # s = s.highlight('name')
        # s = s.highlight('address')
        # # 获取当前页
        # s = s[page - 1: 10]
        # # 只保留以下字段
        # s = s.source(
        #     fields=[
        #         'name', 'address', 'city', 'state',
        #         'postal_code', 'neighborhood', 'stars',
        #         'review_count', 'location', 'is_open'
        #     ])
        start_time = datetime.now()
        try:
            s = Search.from_dict(query_dict)
            response = s.execute()
        except ConnectionError:
            return JsonResponse(CustomResponseJson(msg='搜索成功', code=0))

        end_time = datetime.now()
        last_time = (end_time - start_time).total_seconds()
        total_nums = response['hits']['total']
        if total_nums % 10 > 0:
            page_nums = int(total_nums / 10) + 1
        else:
            page_nums = int(total_nums / 10)

        if page < total_nums:
            has_next = True
        else:
            has_next = False

        hit_list = response.hits.hits
        restaurant_list = list()
        data = dict(
            last_time=last_time, page_nums=page_nums,
            key_words=key_words, total_nums=total_nums,
            data=restaurant_list, has_next=has_next
        )
        for hit_dict in hit_list:
            restaurant_id = hit_dict.get('_id', None)
            restaurant_info = hit_dict.get('_source', None)
            highlight = hit_dict.get('highlight', None)
            if restaurant_info is not None and restaurant_id is not None and highlight is not None:
                restaurant_info['id'] = restaurant_id
                name = highlight.get('name', None)
                address = highlight.get('address', None)
                if name is not None:
                    restaurant_info['name'] = name[0]
                if address is not None:
                    restaurant_info['address'] = address[0]
                restaurant_list.append(restaurant_info)
        return JsonResponse(CustomResponseJson(msg='搜索成功', code=1, data=data))
