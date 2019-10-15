CREATE PROCEDURE get_data @start_time Varchar(20),@end_time Varchar(20),@column VARCHAR(10)
AS
   
   exec('SELECT column3,'+@column+' FROM market_data
   WHERE column3 > '''+
   @start_time+'''AND column3 <'''+ @end_time+'''')
   
go

drop procedure get_data
EXEC get_data '2008-1-1','2009-2-2','column5'