from django import template
from django.utils.safestring import mark_safe

from mainapp.models import Smartphone


register = template.Library()


TABLE_HEAD = """
                <table class="table">
                  <tbody>
             """

TABLE_TAIL = """
                  </tbody>
                </table>
             """

TABLE_CONTENT = """
                    <tr>
                      <td>{name}</td>
                      <td>{value}</td>
                    </tr>
                """

PRODUCT_SPEC = {
    'notebook': {
        'Diagonal': 'diagonal',
        'Displey turi': 'display_type',
        'CPU chastotasi': 'processor_freq',
        'Operativ xotira': 'ram',
        'Video karta': 'video',
        'Batareya quvvati': 'time_without_charge'
    },
    'smartphone': {
        'Diagonal': 'diagonal',
        'Displey turi': 'display_type',
        'Ekran olchamlari': 'resolution',
        'Batareya quvvati': 'accum_volume',
        'Operativ xotira': 'ram',
        'SD-karta hajmi': 'sd',
        'SD-kartaning maksimal hajmi': 'sd_volume_max',
        'Kamera (MP)': 'main_cam_mp',
        'Old kamera (MP)': 'frontal_cam_mp'
    }
}


def get_product_spec(product, model_name):
    table_content = ''
    for name, value in PRODUCT_SPEC[model_name].items():
        table_content += TABLE_CONTENT.format(name=name, value=getattr(product, value))
    return table_content


@register.filter
def product_spec(product):
    model_name = product.__class__._meta.model_name
    if isinstance(product, Smartphone):
        if not product.sd:
            PRODUCT_SPEC['smartphone'].pop('Максимальный объем SD карты', None)
        else:
            PRODUCT_SPEC['smartphone']['Максимальный объем SD карты'] = 'sd_volume_max'
    return mark_safe(TABLE_HEAD + get_product_spec(product, model_name) + TABLE_TAIL)

