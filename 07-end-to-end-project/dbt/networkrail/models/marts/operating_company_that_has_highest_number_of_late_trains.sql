with

fct_movements as (

    select * from {{ ref('fct_movements')}}
)

, final as (

    select
        company_name
        , count(variation_status) as count_variation_status

    from fct_movements
    where variation_status in ('LATE')
    group by company_name
    order by count_variation_status desc

)

select * from final