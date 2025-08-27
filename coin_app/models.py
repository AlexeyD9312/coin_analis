from django.db import models
import os

class CoinInfo(models.Model):
    ticker = models.CharField(max_length=10, unique=True)      
    name = models.CharField(max_length=100, unique=True)       
    logo = models.ImageField(upload_to="coins_logos/")         
    foundation_year = models.PositiveIntegerField()            
    founder = models.CharField(max_length=200, blank=True, null=True)   
    description = models.TextField(blank=True, null=True)     # Описание

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.ticker})"


class CoinsData(models.Model):
    coin = models.ForeignKey(
        CoinInfo,
        to_field="ticker",          # связь по тикеру
        db_column="ticker",         # колонка в БД будет называться "Ticker"
        on_delete=models.CASCADE,
        related_name="market_data",
        null=True,
        blank=True
    )
    Name = models.CharField(max_length=100, blank= False, null=False, unique= True)
    ticker = models.CharField(max_length=10, blank= False, null=False, unique= True, db_column='Ticker')
    interval = models.CharField(max_length=10)
    timestamp = models.DateTimeField(blank=True, null=True)
    open_price = models.DecimalField(max_digits=20, decimal_places=2)
    hihg_price = models.DecimalField(max_digits=20, decimal_places=2)
    low_price = models.DecimalField(max_digits=20, decimal_places=2)
    close_price = models.DecimalField(max_digits=20, decimal_places=2)
    vwap = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    volume = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    trade_count = models.IntegerField(blank=True, null=True)

    class Meta:
        unique_together = ('ticker', 'interval', 'timestamp')
        indexes = [
            models.Index(fields=['ticker', 'interval', 'timestamp'])
        ]
        permissions = [
            ('can_addministrate_lib','User can administrate coin DB'),
            ('can_correct_info', 'User can correct some price')
        ]
        ordering = ['Name']

    def save(self, *args, **kwargs):
        if self.Name:
            self.Name = self.Name.capitalize()
        if self.ticker:
            self.ticker = self.ticker.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.ticker} {self.interval} {self.timestamp}"
    

class UploadedFiles(models.Model):
    file = models.FileField(upload_to='uploads/')
    filename = models.CharField(max_length=255)
    word_count = models.IntegerField()
    char_count = models.IntegerField()
    uploaded_at = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return self.filename
    
    def delete(self, *args, **kwargs):
        if self.file:
            if os.path.exists(self.file.path):
                os.remove(self.file.path)
        super().delete(*args, **kwargs)
