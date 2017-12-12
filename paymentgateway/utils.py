import hashlib
from datetime import datetime
from paymentgateway.models import Configuration as PGConf
from django.forms.models import model_to_dict

class PayGen(object):
    """
        payment txn id generator
        payment unique hash value generator

    """
    @staticmethod
    def generate_txn_id(str_hash):
        """
            generate a unique transaction id from the first 30 digits of hash of email+mobile

        """
        hash_object = hashlib.sha256(str_hash)
        return hash_object.hexdigest()[:30]


    @staticmethod
    def generate_hash(data, hashSequence):
        """
            generate a unique hash required by payU as per the configuration

        """
        hash_string = "|".join([data.get(x, '') for x in hashSequence.split('|')])
        return hashlib.sha512(hash_string).hexdigest().lower()


def get_payment_params(service_provider, leaddata):
    """
        # generate txnid
        # generate hash from the config params provided
        # fetch payment configuration and return params dict,
        # which contains hash and txn id

    """
    string_for_hash = "%s-%s-%s" % (leaddata['email'], leaddata['phone'], datetime.now())
    if service_provider == 'payu_paisa':
        pgconf = PGConf.objects.get(service_provider=service_provider)
        data = model_to_dict(pgconf)
        data.update(leaddata)
        # prepare hash
        txnid = PayGen.generate_txn_id(string_for_hash)
        data['txnid'] = txnid
        data.update({
            'txnid': txnid,
            'hash': PayGen.generate_hash(data, pgconf.hash_params_list)
        })

        return data
