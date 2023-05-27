with

fct_movements as (

    select * from {{ ref('fct_movements')}}
)

, final as (

    select
        train_id
        , count(offroute_ind) as count_off_route

    from fct_movements
    where offroute_ind = true
    group by train_id
    order by count_off_route desc

)

select * from final