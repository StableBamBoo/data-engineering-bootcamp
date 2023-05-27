with

fct_movements as (

    select * from {{ ref('fct_movements')}}
)

, not_late_and_off_route as (

    select
    distinct company_name
    -- , count(variation_status) as count_variation_status

    from fct_movements
    where variation_status not in ('LATE', 'OFF ROUTE')
    group by company_name
    -- order by count_variation_status desc

)

, final as (

    select
        distinct a.company_name

    from fct_movements as a
    join not_late_and_off_route as f
    on a.company_name = f.company_name

)

select * from final