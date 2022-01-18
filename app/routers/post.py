from typing import List, Optional
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.sql.expression import false
from sqlalchemy.sql.sqltypes import Boolean
# to join /create model to main file
from ..import models
from ..database import engine,SessionLocal
from sqlalchemy import func
from sqlalchemy.orm import Session
import time
from ..database import get_db
from ..utils import hash
from ..schemas import PostBase,PostCreate,PostResp,Postt
from ..oauth2 import get_current_user 
# defining router to connect with main file

router=APIRouter(
    prefix="/posts",
    tags=["Posts"]
)





# creating ne function to get/display all post
@router.get('/',response_model=List[PostResp])
# @router.get('/')
def posts(db: Session = Depends(get_db),limit:int=100,search:Optional[str]=""):
    # limit variable is define to use query / we used this to show post equal to limit no. in path operation we set query in path in postman like usrl?variable=no.
    # we can add as many query as we want like above
    # to get all posts from database
    # cursor.execute(""" SELECT * FROM posts""")
    # posts=cursor.fetchall()   Or
# ------------------------------------------------------------------
    # fetching posts by using ORM sqlalchemy
    # posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).all()
    posts_new=db.query(models.Post,func.count(models.Vote.post_id).label('votes')).join(models.Vote, 
        models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).all()
    if len(posts_new)==0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No Posts")
   
    
    return posts_new
# -==============================================================================================================
# -==============================================================================================================
# creat function to fetch only users posts
@router.get("/my_posts",response_model=List[PostResp])
def my_post(db:Session=Depends(get_db),current_user:int =Depends(get_current_user)): 
    
    # posts=db.query(models.Post).filter(models.Post.auther_id==current_user.id).all()
    posts=db.query(models.Post,func.count(models.Vote.post_id).label('votes')).join(models.Vote, 
        models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.auther_id==current_user.id).all()
    if posts==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No Posts")
    return posts
# -==============================================================================================================
# -==============================================================================================================


#creating post using basemodel by defining schma for user by creating class BAseModel as shown above
@router.post("/",status_code=status.HTTP_201_CREATED) #we have to convert response_model in list bcoz we want to show list of posts
# adding get_current_user to only login user create post
def new_post(post:PostCreate, db: Session = Depends(get_db),current_user:int =Depends(get_current_user)):
    # creating post using ORM
    # new_post=models.Post(title=post.title,content=post.content) 
    #another way of getting data from database and convert into requires field like above new_post variable is show below
    new_post=models.Post(auther_id=current_user.id, **post.dict())
    # to add post in db
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
# --------------------------------------------------------------------------------
    # creating post using database
    # cursor.execute("""INSERT INTO posts (title,content) VALUES (%s,%s) RETURNING* """,(post.title,post.content))
    # new_post=cursor.fetchone()
    # conn.commit()
   
# ----------------------------------------------------------------------------------

    # post_dict=post.dict()
    # post_dict['id']=randrange(0,100000)
    # my_posts.append(post_dict)
    # print(posts)
    # print(posts.dict())
    # my_posts.append(post.dict())
    # return {"new post": post_dict}

# -==============================================================================================================

#creating funvtion to fetch one post at time
@router.get("/{id}")
# @router.get("/{id}",response_model=PostResp)
def get_post(id:int, db: Session = Depends(get_db)):
    # to get/open one post from database
    # cursor.execute(""" SELECT * FROM posts WHERE id=%s """,(str(id)),)
    # post=cursor.fetchone()
    # # print(id)
    # post=find_post(id)
# --------------------------------------------------------------------------------
    # fetching post by orm model/get one post at time using ORM
    post=db.query(models.Post,func.count(models.Vote.post_id).label('votes')).join(models.Vote, 
        models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    # post=db.query(models.Post).filter(models.Post.id == id).first()
# --------------------------------------------------------------------------------
  
    # if post id not available
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Page Not Found")
        
        # response.status_code= status.HTTP_404_NOT_FOUND
        # return {"message":"Page Not Found"}
        # or
       
    return  post

# -==============================================================================================================


# to delete post
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session = Depends(get_db),current_user:int =Depends(get_current_user)):
    
# --------------------------------------------------------------------------------
    
    # to delet post from database using sql query
    # cursor.execute(""" DELETE FROM posts WHERE id=%s RETURNING *""",(str(id)))
    # delet_post=cursor.fetchone()
    # conn.commit()
# --------------------------------------------------------------------------------
# delete post using ORM sql alchemy
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()

    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post Not Exist")
    if post.auther_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not valid action")
    post_query.delete(synchronize_session=False)
    db.commit()
    #find index of post in array to delete
    # index=index_post(id)
    # if index==None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post Not Exist")
    # my_posts.pop(index)
    return Response(status_code= status.HTTP_204_NO_CONTENT)
# -==============================================================================================================


#to update post

@router.put("/{id}")
def update_post(id:int,updt_post:PostCreate,db: Session = Depends(get_db),current_user:int =Depends(get_current_user)):
    # update post in database usin sql query
    # cursor.execute("""UPDATE posts SET title=%s,content=%s WHERE id=%s RETURNING *""",(post.title,post.content,(str(id))),)
    # updated_post=cursor.fetchone()
    # conn.commit()
    # index=index_post(id)
# --------------------------------------------------------------------------------
#    updating post using ORM
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()
    
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post Not Exist")    
    if post.auther_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not valid action")
    post_query.update(updt_post.dict(), synchronize_session=False)
    db.commit()
    # post_dict=post.dict()
    # post_dict['id']=id
    # my_posts[index]=post_dict
    return post_query.first()

