'use strict';

import Dispatcher from '../dispatcher';
import {inbox} from '../endpoints';
import setToString from '../lib/settostring';
import {token} from '../users/actions';
import * as api from '../api';

/**
 * Get all
 */
export function getAll(user = null, application = null) {
  let request = api.get(inbox.index(user, application), { token });

  return Dispatcher.dispatch(getAll, request);
}

/**
 * Delete
 */
export function remove(uuid, application = null, user = '@me') {
  let request = api.del(inbox.delete(uuid, application, user), { token });

  return Dispatcher.dispatch(remove, request);
}

// Override toString methods. Pretty useful for dispatched actions monitoring.
setToString('inbox', {
  getAll,
  remove
});
