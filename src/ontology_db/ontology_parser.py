#!/usr/bin/env python
# -*- coding: utf-8 -*-

from openpyxl import load_workbook
from entities.db_config.base import Base, Session, engine
from entities.scales import Scale, Scale_value

# Instead of DB we use json file to test the module
import json


# generate database schema
Base.metadata.create_all(engine)

# start session
session = Session()

# ontology file
FILE_NAME = './ontology.xlsm'


# creating a dict of {scale: [values]} from ontology file
def parse_scales(file_name):
    # Load in the workbook
    ws = load_workbook(file_name)['Scales']
    scales = {}
    row_max = 65

    for row in range(1, row_max):
        col = 1

        if ws.cell(row, col).value == 'Title':
            scale_name = ws.cell(row, col + 1).value
            continue

        elif ws.cell(row, col).value == 'Values':
            values = []

            while ws.cell(row, col + 1).value is not None:
                col += 1
                values.append(str(ws.cell(row, col).value))

            scales[scale_name] = values[:]

        else:
            continue

    return scales


def insert_scales_data(data):
    for scale in data.keys():
        for value in data[scale]:
            session.add(Scale_value(value, Scale(scale)))

    session.commit()
    session.close()
    print('\nScales are successfully parsed and moved to db\n')


def parse_objects(file_name):
    pass


def insert_object_data(data):
    pass


# local tests with queries
def test_scales():
    ontology_scales = {}

    all_scales = session.query(Scale) \
        .all()

    # set of all scale names
    all_scale_names_set = set([i.name for i in all_scales])

    for scale_name in all_scale_names_set:
        scale_values = session.query(Scale_value) \
            .join(Scale) \
            .filter(Scale.name == scale_name) \
            .all()

        values = []

        for scale_value in scale_values:
            values.append(scale_value.value)

        ontology_scales[scale_name] = values

    print('\n### All scales:\n', ontology_scales)


def test_objects():
    pass


def clear_data(session):
    meta = Base.metadata
    for table in reversed(meta.sorted_tables):
        print('Clear table %s' % table)
        session.execute(table.delete())
        session.commit()


def ontology_parser():
    clear_data(session)
    insert_scales_data(parse_scales(FILE_NAME))
    test_scales()

    # for row in ws.iter_rows(min_row=1, max_col=100, max_row=100):
    #     for cell in row:
    #         if cell.value == 'Title':
    #             pass

    #         elif cell.value == 'Values'

    # ontology = {}

    # for row in ws.iter_rows(min_row=2, max_col=12, max_row=45):
    #     object_features = []
    #     for cell in row:
    #         object_features.append(cell.value)

    #     entity = object_features.pop(1)
    #     ontology[entity] = object_features[0:]

    # return ontology


def main():
    ontology_parser()


if __name__ == '__main__':
    main()
