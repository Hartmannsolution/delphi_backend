from nis import cat
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from . import models, schemas

    
def get_answer(db: Session, answer_id: int):
    return db.query(models.Answer).filter(models.Answer.id == answer_id).first()

def get_category(db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.id == category_id).first()

def get_category_by_name(db: Session, category_name: str):
    category = db.query(models.Category).filter(models.Category.name == category_name).first()
    if category is None:
        return create_category(db, schemas.CategoryBase(name=category_name, description=""))
    return category

def get_answers_by_class(db: Session, class_name: str):
    return db.query(models.Answer).filter(models.Answer.class_name == class_name).all()

def get_answers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Answer).offset(skip).limit(limit).all()

def create_answer(db: Session, answer: schemas.Answer):
    db_answer = models.Answer(uuid = answer.uuid, text=answer.text, class_name=answer.class_name, is_positive=answer.is_positive, count=0)
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer

def create_category(db: Session, category: schemas.Category):
    db_category = models.Category(name=category.name, description=category.description)
    try:
        db.add(db_category)
        db.commit()
    except Exception as e:
        db.rollback()
        return None
    db.refresh(db_category)
    return db_category

def create_class(db: Session, class_name: schemas.ClassNameBase):
    new_class = models.Class_name(name=class_name.name, count=class_name.count)
    try:
        db.add(new_class)
        db.commit()
    except Exception as e:
        db.rollback()
        return None
    db.refresh(new_class)
    return new_class

def terminate_delphi(db: Session, class_name: str, new_class_name: str):
    """Terminate this evaluation by changing the classname on all the answers of the class. Thereby making it impossible to post more answers and to rate the answers"""
    all_answers = db.query(models.Answer).filter(models.Answer.class_name == class_name).all()
    newclass = create_class(db, schemas.ClassNameBase(name=new_class_name))
    for ans in all_answers:
        ans.class_name = new_class_name
        db.add(ans) # when you Session.add() a transient instance, it becomes "pending".
    classname = db.query(models.Class_name).filter(models.Class_name.name==class_name).first()
    # classname.name = new_class_name
    # db.add(classname)
    db.delete(classname)
    try:
        db.commit()
    except Exception as e:
        print('ERROR',e)
        db.rollback()
        return None
    return "TERMINATED"


def increment_answer(db: Session, answer_id: int, number: int):
    answer: models.Answer = db.query(models.Answer).filter(models.Answer.id == answer_id).first()
    if answer is None:
        print('No answer with id: '+str(answer_id))
        return
    count: int = answer.count + number
    answer.count = count
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        return None
    return answer

def is_valid_class(db: Session, class_name:str):
    return db.query(models.Class_name).filter(models.Class_name.name == class_name).first() != None

def add_category(db: Session, answer_id, category_name):
    a = get_answer(db=db, answer_id=answer_id)
    if answer_id is None:
        raise Exception('No answer by id: '+str(answer_id))
    c = get_category_by_name(db=db, category_name=category_name)
    c.answers.append(a)
    db.commit()
    db.refresh(a)
    return a

def comment_answer(db: Session, answer_id:int, comment:str):
    answer: models.Answer = db.query(models.Answer).filter(models.Answer.id == answer_id).first()
    if answer is None:
        print('No answer with id: '+str(answer_id))
        return
    answer.comment = comment
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        return None
    return answer


if __name__ == "__main__":
    engine = create_engine(
        "postgresql://dev:ax2@db:5432/app", # connect_args={"check_same_thread": False} # only for sqllite
    )
    db = sessionmaker(autocommit=False, autoflush=False, bind=engine)() # create a database session, that can be closed after use. For use of session pool - see: main.get_db() with yield and finally block.
    result = create_class(db=db, class_name=schemas.ClassName(name="someclass"))
    print(result)
    result = create_answer(db=db, answer=schemas.AnswerBase(uuid="UIIDDDHHO", text="POSITIVT Dette er en lang text, som er meget positiv og som har fine elementer af lyrisk kvalitet, med undertoner af satirisk samfundskritik og meta kognitive overvejelser omkring kvaliteten af det sagte og det italesatte", class_name="someclass", is_positive=True))
    result = create_answer(db=db, answer=schemas.AnswerBase(uuid="HOHOHOIIIDDHHKD", text="NEGATIVT: Kan vi lige se på hvordan bla bla bla bla bla bla bla bla bla bla", class_name="someclass", is_positive=False))
    result = create_answer(db=db, answer=schemas.AnswerBase(uuid="CHCHCHCHCH", text="POSITIVT hov hov hov dette er da alt for fedt", class_name="someclass", is_positive=True))
    result = create_answer(db=db, answer=schemas.AnswerBase(uuid="LDLSLDDHSH", text="NEGATIVT: Dette er en meget lang tekst på virkelig mange linjer, eller i hvert fald med en hel del ord i, som ikke i sig selv har den store betydning, men som alligevel heller ikke kun er det rene sludder. Her kunne måske fyldes mere meningsindhold ind, men på den anden side er ideen mere bare at have en meget lang tekst som man kan se i frontend applikationen. Det er ikke for at sige noget ondt men jeg synes godt de andres evalueringer kunne have været lidt længere", class_name="someclass", is_positive=False))
    result = create_category(db=db, category=schemas.CategoryBase(name="Material", description="Docker notebooks"))
    result = get_answers(db = db, skip=1, limit=2)
    # result_answer = add_category(db=db, answer_id=1, category_name='Materialus')
    # print('updated answer with category',result_answer)
    # result = get_answers_by_class(db=db, class_name="someclass")
    # print('BY CLASS: ',result)
    result = increment_answer(db, 1,4)
    # result = increment_answer(db, 2,8)
    # result = increment_answer(db, 3,2)
    # print('Incremented!!!:',result)
    result = comment_answer(db, 1, "Dette er min kommentar til Statement 1")
    # result = terminate_delphi(db, "someclass", "someotherclass")
    # print(result)
    print(is_valid_class(db,"someotherclass"))
    db.close()
