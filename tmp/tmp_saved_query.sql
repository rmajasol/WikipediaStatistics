select date(f_date_time), substr(dayname(f_date_time),1,2), f_lang_id, f_ns_id, count(*) from Filtered where f_action_id = 2 group by date(f_date_time), f_lang_id, f_ns_id;