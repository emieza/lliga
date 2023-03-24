from django.db import models

# Create your models here.

class Equip(models.Model):
    nom = models.CharField(max_length=200)
    detalls = models.TextField(null=True,blank=True)
    ciutat = models.CharField(max_length=100)
    def __str__(self):
        return self.nom

class Lliga(models.Model):
    titol = models.CharField(max_length=200)
    detalls = models.TextField(null=True,blank=True)
    inici = models.DateField()
    final = models.DateField()
    equips = models.ManyToManyField(Equip)
    def __str__(self):
        return self.titol

class Jugador(models.Model):
    nom = models.CharField(max_length=50)
    alias = models.CharField(max_length=50)
    cognom1 = models.CharField(max_length=50)
    cognom2 = models.CharField(max_length=50)
    detalls = models.TextField(null=True,blank=True)
    def __str__(self):
        equip_actual = self.fitxa_set.filter(final=None).first()
        return "{} {} \"{}\" ({})".format(self.nom,self.cognom1,
                self.alias,equip_actual.equip)

class Fitxa(models.Model):
    equip = models.ForeignKey(Equip,null=True,
                    on_delete=models.SET_NULL)
    jugador = models.ForeignKey(Jugador,null=True,
                    on_delete=models.SET_NULL)
    inici = models.DateField()
    final = models.DateField(null=True,blank=True)
    dorsal = models.IntegerField()
    def __str__(self):
        return "{} : {} {}".format(self.equip,self.jugador.nom,self.jugador.cognom1)

class Partit(models.Model):
    class Meta:
        unique_together = ["local","visitant","lliga"]
    local = models.ForeignKey(Equip,on_delete=models.CASCADE,
                    related_name="partits_local")
    visitant = models.ForeignKey(Equip,on_delete=models.CASCADE,
                    related_name="partits_visitant")
    lliga = models.ForeignKey(Lliga,on_delete=models.CASCADE)
    detalls = models.TextField(null=True,blank=True)
    inici = models.DateTimeField(null=True,blank=True)
    def __str__(self):
        return "{} - {}".format(self.local,self.visitant)
    def gols_local(self):
        return self.event_set.filter(
            tipus=Event.EventType.GOL,equip=self.local).count()
    def gols_visitant(self):
        return self.event_set.filter(
            tipus=Event.EventType.GOL,equip=self.visitant).count()

class Event(models.Model):
    class EventType(models.TextChoices):
        GOL = "GOL"
        AUTOGOL = "AUTOGOL"
        FALTA = "FALTA"
        PENALTY = "PENALTY"
        MANS = "MANS"
        CESSIO = "CESSIO"
        FORA_DE_JOC = "FORA_DE_JOC"
        ASSISTENCIA = "ASSISTENCIA"
        TARGETA_GROGA = "TARGETA_GROGA"
        TARGETA_VERMELLA = "TARGETA_VERMELLA"
    partit = models.ForeignKey(Partit,on_delete=models.CASCADE)
    temps = models.TimeField()
    tipus = models.CharField(max_length=30,choices=EventType.choices)
    jugador = models.ForeignKey(Jugador,null=True,
                    on_delete=models.SET_NULL,
                    related_name="events_fets")
    equip = models.ForeignKey(Equip,null=True,
                    on_delete=models.SET_NULL)
    # per les faltes
    jugador2 = models.ForeignKey(Jugador,null=True,blank=True,
                    on_delete=models.SET_NULL,
                    related_name="events_rebuts")
    detalls = models.TextField(null=True,blank=True)

