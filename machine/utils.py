from .models import Material_state,Machine

def update_material(machine_id):
    data = Material_state.objects.filter(machine_id = machine_id).order_by('margin').first()
    data = data.get_json()
    margin = data['margin']
    margin = float(margin)
    margin = int(margin)
    print (margin)
    if margin < 200:
        update_material = Machine.objects.filter(pk = machine_id).update(material_state = '3')
    if margin> 500:
        update_material = Machine.objects.filter(pk = machine_id).update(material_state = '1')
    if margin >= 200 and margin <= 500:
        update_material = Machine.objects.filter(pk = machine_id).update(material_state = '2')
    return None

