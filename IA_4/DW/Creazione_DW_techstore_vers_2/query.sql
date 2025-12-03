select dd.anno, sum(ricavi)
from fact_vendite fv
join  dim_data dd on fv.data_sk = dd.data_sk 
group by dd.anno;

select dd.anno, dd.mese, dp.categoria, sum(fv.ricavi)
from fact_vendite fv
join dim_data dd on fv.data_sk = dd.data_sk
join dim_prodotto dp on fv.prodotto_sk = dp.prodotto_sk
group by dd.anno, dd.mese, dp.categoria
order by dd.anno, dd.mese;


select dc.cliente_sk, dc.nome, dc.cognome, sum(fv.ricavi) as speso
from fact_vendite fv
join dim_cliente dc on fv.cliente_sk = dc.cliente_sk
group by dc.cliente_sk
order by speso desc
limit 10;

select dp.prodotto_sk, dp.nome, dp.categoria, avg(fv.ricavi) as media_ricavi
from fact_vendite fv
join dim_prodotto dp on fv.prodotto_sk = dp.prodotto_sk
group by dp.prodotto_sk, dp.categoria
order by media_ricavi desc;


with tempo as(
	select ds.spedizione_sk, (ds.data_consegna - ds.data_spedizione) as tempo_consegna
	from dim_spedizione ds
	group by ds.spedizione_sk
)
select ds.corriere, avg(tempo_consegna) as t_m_consegna
from fact_vendite fv
join dim_spedizione ds on fv.spedizione_sk = ds.spedizione_sk
join tempo t on fv.spedizione_sk = t.spedizione_sk
group by ds.corriere
order by t_m_consegna desc;

select dc.fascia_eta, sum(ricavi) as ricavi_tot
from fact_vendite fv
join dim_cliente dc on fv.cliente_sk = dc.cliente_sk
group by dc.fascia_eta
order by ricavi_tot desc;

-- anno, categoria, ricavi_tot, quantit_tot, ticket_medio
select dd.anno, dp.categoria, 
	sum(fv.ricavi) as ricavi_tot, 
	sum(fv.quantita) as quantita_tot,
	(sum(fv.ricavi)/sum(fv.quantita)) as ticket_medio
from fact_vendite fv
join dim_data dd on dd.data_sk = fv.data_sk
join dim_prodotto dp on dp.prodotto_sk = fv.prodotto_sk
group by dd.anno, dp.categoria
order by dd.anno, dp.categoria, ticket_medio desc;

-- regione, categoria, ricavi_tot, scontrino_medio per ordine, anno=2024
select dp.categoria,  dc.regione, sum(fv.ricavi) as ricavi_tot, 
	(sum(fv.ricavi)/count(distinct fv.ordine_id)) as scont_med, count(distinct fv.ordine_id)
from fact_vendite fv
join dim_data dd on dd.data_sk = fv.data_sk
join dim_prodotto dp on dp.prodotto_sk = fv.prodotto_sk
join dim_cliente dc on dc.cliente_sk = fv.cliente_sk
where dd.anno = 2024
group by dc.regione, dp.categoria
order by ricavi_tot desc;

