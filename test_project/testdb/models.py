from django.db import models

def format_number(val):
    if isinstance(val, float) and val.is_integer():
        return str(int(val))
    else:
        return str(val)


# Create your models here.
class Bearings(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    d_bore = models.FloatField(db_column='d bore')
    d_outside = models.FloatField(db_column='D outside')
    b = models.FloatField(db_column='B')
    dynamic = models.FloatField()
    static = models.FloatField()
    ref_speed = models.IntegerField(db_column='Reference speed')
    lim_speed = models.IntegerField(db_column='Limiting speed')

    class Meta:
        db_table = 'bi_cau'

    def __str__(self):
        return self.name

    @classmethod
    def filter_by_my_field(cls, d_bore=None, d_outside=None, b=None):
        # return cls.objects.filter(my_field=value)
        if not d_bore and not d_outside and not b:
            return None
        records = cls.objects.using('bearings').all()
        if d_bore:
            records = records.filter(d_bore=d_bore)

        if d_outside:
            records = records.filter(d_outside=d_outside)

        if b:
            records = records.filter(b=b)

        return [
            {'id': record.id,
             'name': record.name,
             'd_bore': format_number(record.d_bore),
             'd_outside': format_number(record.d_outside),
             'b': format_number(record.b)
             }
        for record in records]
