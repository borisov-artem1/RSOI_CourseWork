from pydantic import ValidationError

from utils.consts import SERVICE


def get_service_name(
  domain_name: str,
) -> str:
  domain_name = domain_name.lower().capitalize()
  service = SERVICE.lower().capitalize()
  return f"{domain_name} {service}"

def remove_extra_symbols(text: str, symbols: str) -> str:
  translate_table = str.maketrans(symbols, "^"*len(symbols))
  return text.translate(translate_table).replace("^", "")

def get_pydantic_validation_error_text(err: ValidationError) -> str:
  errors = err.errors()
  text = remove_extra_symbols(
    text="; ".join(f"{e['loc']}: {e['msg']}" for e in errors),
    symbols="()[],",
  )
  
  return text
