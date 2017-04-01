# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 22:14:54 2016

@author: Darren
"""
import MySQLdb

def CheckBookAvailability(Isbn):
    sql_query_has_book='SELECT * FROM BOOK WHERE BOOK.Isbn="'+str(Isbn)+'";'
    sql_query='SELECT * FROM BOOK_LOANS WHERE BOOK_LOANS.Isbn="'+str(Isbn)+'";'
    sql_query2='SELECT * FROM BOOK_LOANS WHERE BOOK_LOANS.Isbn="'+str(Isbn)+'" AND Date_in is not null AND Date_in<curdate();'
#if a book has never been borrowed or has been returned, will get empty, is avilable
    try:
        conn=MySQLdb.connect("localhost",'root','root','Library',port=3306)
        cur=conn.cursor()
        #check if this library has this book
        cur.execute(sql_query_has_book)
        conn.commit()
        result0=cur.fetchall()
        if(len(result0)==0):
            result_final=[False,'We don\'t have this book in our library!']
            return result_final
        #check if it has been borrowed by someone else
        cur.execute(sql_query)
        conn.commit()
        result=cur.fetchall()
        cur.execute(sql_query2)
        conn.commit()
        result2=cur.fetchall()
        cur.close()
        conn.close()
        if(len(result)==0):
            #don't have this book
            result_final=[True]
            return result_final
        elif(len(result2)==0):
            #have this book but is borrowed by someone else
            message="Sorry, this book has been borrowed by someone else and should be returned before "
            result_final=[False,message+str(result[4])]
            return result_final
        else:
            #have this book, borrowed by someone but has been returned
            result_final=[True]
            return result_final
    except MySQLdb.Error,e:
        print("Failed to connect to MySQL:%d:%s" %(e.args[0],e.args[1]))
#@csrf_exempt
def NumberOfActiveBorrowedBooks(Card_id):
    sql_query='SELECT COUNT(*) FROM BOOK_LOANS WHERE BOOK_LOANS.Card_id="'+str(Card_id)+'" AND \
    Date_in is null;'
    try:
        conn=MySQLdb.connect("localhost",'root','root','Library',port=3306)
        cur=conn.cursor()
        cur.execute(sql_query)
        conn.commit()
        result=cur.fetchone()
        cur.close()
        conn.close()
        return result[0]<3
    except MySQLdb.Error,e:
        print("Failed to connect to MySQL:%d:%s" %(e.args[0],e.args[1]))
#@csrf_exempt
def HasUnpaidFine(Card_id):
#    sql_query_fine='SELECT * FROM BOOK_LOANS,FINES WHERE BOOK_LOANS.Card_id\
#    ="'+str(Card_id)+'" AND BOOK_LOANS.Loan_id=FINES.Loan_id AND Paid="False";'
    sql_query_fine='SELECT * FROM BOOK_LOANS,FINES WHERE BOOK_LOANS.Card_id\
    ="'+str(Card_id)+'" AND BOOK_LOANS.Loan_id=FINES.Loan_id AND Paid=1;'
    try:
        conn=MySQLdb.connect("localhost",'root','root','Library',port=3306)
        cur=conn.cursor()
        cur.execute(sql_query_fine)
        conn.commit()
        result=cur.fetchall()
        unpaid_fine_num=len(result)
        
        cur.close()
        conn.close()
        return unpaid_fine_num>0
    except MySQLdb.Error,e:
        print("Failed to connect to MySQL:%d:%s" %(e.args[0],e.args[1]))

#@csrf_exempt
def HasOverdueBook(Card_id):
    sql_query_overdue='SELECT * FROM BOOK_LOANS WHERE BOOK_LOANS.Card_id\
    ="'+str(Card_id)+'" AND BOOK_LOANS.Due_date<curdate() AND Date_in is null;'
    try:
        conn=MySQLdb.connect("localhost",'root','root','Library',port=3306)
        cur=conn.cursor()
        cur.execute(sql_query_overdue)
        conn.commit()
        result=cur.fetchall()
        overdue_num=len(result)        
        
        cur.close()
        conn.close()
        return overdue_num>0
    except MySQLdb.Error,e:
        print("Failed to connect to MySQL:%d:%s" %(e.args[0],e.args[1]))