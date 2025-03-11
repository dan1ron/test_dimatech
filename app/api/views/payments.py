import hashlib

from fastapi import APIRouter, HTTPException, status

from app.api import deps, schemas
from app.conf import settings
from app.database import crud

router = APIRouter()


@router.post('/webhook', responses={400: {'model': schemas.Message}})
async def webhook(payment: schemas.Payment, db: deps.SessionDep):
    data_to_sign = f'{payment.account_id}{payment.amount}{payment.transaction_id}{payment.user_id}{settings.signature_secret_key}'
    expected_signature = hashlib.sha256(data_to_sign.encode()).hexdigest()
    if payment.signature != expected_signature:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Invalid signature')

    try:
        existing_payment = await crud.get_payment_by_transaction_id(db, transaction_id=payment.transaction_id)
        if existing_payment:
            raise HTTPException(status_code=400, detail='Payment with this transaction_id already exists')

        db_payment = await crud.create_payment(db, payment)
    except HTTPException as err:
        raise err
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))

    return {'message': 'Payment processed successfully', 'payment': db_payment}
